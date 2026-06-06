# 程式碼維運代理：用於軟體維護的 AI Harness 系統設計

## 摘要
本報告提出一個用於軟體維護的 AI Harness 系統，名稱為「程式碼維運代理」（Code Operations Agent）。此系統面向 CI 失敗排查、回歸錯誤診斷、缺陷分析與修補規劃等維運工作。設計重點不在模型訓練，而在於如何讓大型語言模型擔任系統控制器，透過 function calling 呼叫外部工具、結合短期與長期記憶，並遵循可解釋的多步驟 workflow 來產生具證據基礎的建議。本文提出三個核心工具、一個混合式 orchestration 機制、明確的安全邊界與離線評估方法。系統目標是縮短 incident triage 時間、提升診斷一致性，並讓維運決策流程更透明。

## 1. 問題定義與應用背景
現代軟體團隊在處理 CI 失敗、版本回歸或執行期錯誤時，經常需要同時檢查 issue tracker、CI logs、pull request 與 source code。真正耗時的部分通常不是最後修改程式碼，而是先判斷應該看哪裡、哪個訊號最可信、下一步該查什麼。這類工作高度依賴工程師經驗，因此不同人處理相似問題時，速度與品質可能差異很大。

本設計選擇的應用場景是軟體維護用的程式碼維運代理。目標使用者包含 on-call engineers、一般軟體工程師，以及需要快速掌握狀況的 tech leads。此系統的核心任務是協助使用者蒐集上下文、縮小問題範圍、產生 root-cause hypothesis，並提出安全的修補方向。

本系統刻意限制範圍，只處理 triage、診斷與 patch planning，不直接執行 merge、deploy 或其他具破壞性的 repository 操作。這個邊界對於安全性和可解釋性都很重要。系統應在 90 秒內提供第一個可執行的診斷建議，同時限制工具呼叫次數以控制成本，並避免在 prompts 或摘要中暴露敏感資訊。

## 2. AI Harness 系統架構
程式碼維運代理由四個主要層次構成：LLM controller、tool layer、memory layer 與 orchestration layer。

LLM controller 是整個系統的核心控制元件。它負責解析使用者請求、決定下一步動作、判斷是否需要呼叫工具、整合中間結果，並輸出最後回應。也就是說，LLM 在這裡不是一般聊天模型，而是受控的 system controller。

Tool layer 提供 LLM 無法單獨可靠完成的外部能力。本設計中包含三個核心工具。第一個是 Issue/PR Context Fetcher，用來取得 issue metadata、相關 pull requests、ownership 與近期討論內容。第二個是 CI Log Analyzer，用來從 workflow logs 中萃取 failure signature 與可能原因。第三個是 Repo Code Search plus Diff Planner，用來定位可疑程式碼區域並提出最小化修補方案。若需要擴充，還可以加入 Runbook Retriever 來讀取標準維運文件或特定服務的 troubleshooting 指南。

Memory layer 分為短期與長期記憶。短期記憶保存當前案件狀態，例如 incident identifier、目前假設、已執行的工具呼叫、未解決問題與 confidence。長期記憶則儲存重複出現的 incident signature、已驗證修復方法與特定服務的維運知識。這種分層設計讓系統既能追蹤當前任務，也能逐步累積跨案件經驗。

Orchestration layer 則負責整體流程控制，包括 state transition、stop conditions、guardrails 與 escalation 規則。整體資料流如下：使用者提出請求後，controller 先進行 intent classification，接著建立 tool plan，然後呼叫工具、整合證據，最後產生建議。相較於完全自由式的 agent loop，這種顯式結構更容易除錯與評估。

## 3. Function Calling 與 Tool Usage 設計
Function calling 是本系統把使用者意圖轉換成實際行動的核心機制。每個工具都必須有清楚的目的、input schema、output schema、觸發條件與失敗後的 fallback 策略。

Issue/PR Context Fetcher 會在使用者提到 bug ticket、incident ID 或 pull request 時啟動。輸入包含 repository 名稱、issue 或 PR identifier，以及時間範圍。輸出則包含標題、狀態、參與者與近期事件。此工具可在深入診斷前提供必要的 operational context。

CI Log Analyzer 會在任務涉及 failed build、failed test 或 deployment error 時觸發。其輸入為 repository、workflow run ID 與 job ID。輸出內容包括 failure signature、關鍵 error lines、可能原因與 confidence score。這個工具的價值在於把雜亂的 raw logs 壓縮成結構化訊號，降低 LLM 直接閱讀長日誌的負擔。

Repo Code Search plus Diff Planner 會在 controller 已形成初步假設後啟動，用來尋找 source-level evidence。輸入為 repository、branch 與 search query；輸出則為 candidate files、suspect functions 以及 patch plan。這個工具不是要取代工程師寫 patch，而是要把排查範圍縮小到最可能的程式碼區域。

所有工具輸出都必須先通過 schema validation。若工具 timeout，controller 會以更小範圍重試一次；若輸出格式錯誤，controller 會要求正規化輸出並重試一次。系統預設為 read-only，所有涉及修改程式碼的內容都屬於 advisory output，必須先經過人工確認。

## 4. 多步驟 Agent Workflow
本系統的 workflow 可分為五個主要階段。

第一階段是 intent understanding。Controller 先將使用者請求分類為 CI failure triage、regression diagnosis、runtime bug investigation 或 patch planning 等類型。不同類型會對應不同的工具需求與證據順序。

第二階段是 planning。Controller 會建立有順序的 tool-call plan、設定工具預算，並定義 stop conditions。這一步的目的在於防止 agent 無限制探索，並讓整個流程具有可審查性。

第三階段是 tool execution。以典型 CI incident 為例，controller 會先呼叫 Issue/PR Context Fetcher 取得背景，再呼叫 CI Log Analyzer 取得 failure signature，最後使用 Repo Code Search plus Diff Planner 進行程式碼定位與修補建議。不過不同 incident 類型不一定都要執行完整三步。

第四階段是 evidence integration。Controller 會比較 issue context、logs 與 repository evidence 之間是否一致。如果三方訊號互相支持，就能形成高信心診斷；若訊號彼此矛盾，系統可以追加一次工具呼叫、降低 confidence，或直接進入 escalation。

第五階段是 final response generation。最終輸出至少應包含可能 root cause、confidence score、最相關的 files 或 functions、修補方向，以及需要注意的風險事項。

Workflow 也包含明確的 branch 與 recovery logic。如果 logs 顯示 flaky test 或非決定性失敗，controller 會走 stability branch，而不是直接進入 patch proposal branch。若錯誤屬於 deterministic compilation failure 或 dependency mismatch，則可以直接朝修補規劃前進。若工具 timeout，系統會縮小範圍重試；若 schema 不合法，系統會先修正格式再重試。案件完成後，系統會把 incident signature 與接受的解法寫入 memory。

## 5. Orchestration 與 Decision Logic
本設計採用混合式 orchestration。State-machine 負責規定可接受的流程轉移，而 LLM 則在每個 state 內做上下文推理。這種做法兼顧了控制能力與彈性。

系統有三個核心 decision checkpoints。第一，檢查使用者請求是否足夠明確，能否安全展開工具呼叫。第二，檢查目前蒐集到的證據是否足以支持診斷。第三，檢查 confidence 是否高到可以提出 patch recommendation，而不只是保留在假設層級。

此外，系統也有清楚的 stop conditions。當證據覆蓋率足夠、工具預算耗盡，或使用者要求轉交人工時，流程就應終止。若 confidence 過低或證據彼此衝突，controller 會升級到 human reviewer，而不是假裝自己已經知道答案。此時系統應輸出 compact evidence pack，包括取得的 context、主要 failure signal、衝突線索與建議下一步。

Observability 也是必要設計。每次工具呼叫、latency、retry 次數、token usage 與 controller decision 都應被記錄下來，作為後續分析與優化依據。

## 6. 評估方法
本系統的評估方式採用離線 historical case set，包含 30 筆軟體維護 incidents，並平衡涵蓋 CI failures、runtime bugs 與 regressions。每一筆案例都應附帶足夠的 repository context、issue 資訊與 logs，讓整個決策流程可以重現。

主要評估指標共有五項。第一是 task completion rate，用來衡量系統能否產出可用的診斷結果。第二是 tool-call accuracy，用來評估 controller 是否選對工具。第三是 root-cause precision@1，用來檢查第一名假設是否正確。第四是 mean time to first actionable recommendation，用來衡量實務上的可用性。第五是 failure recovery success rate，用來評估系統在工具 timeout 或輸出不完整時是否仍然能提供幫助。

評分可以使用 0 到 2 分的尺度，從 diagnosis quality、actionability 與 safety compliance 三個面向給分。0 分表示錯誤或不安全，1 分表示部分正確但實用性不足，2 分則表示正確、具證據基礎且可實際採取行動。

Baseline 可以設計成不具 tool access 的 LLM-only assistant。這個比較很重要，因為本作業強調的是 orchestration 與 tool use。如果 AI Harness 能在 precision、actionability 與 failure recovery 上明顯優於 baseline，就能有效證明此系統設計的價值。

系統優化流程則採標準工程方式：定期回顧低分案例、檢查 routing 或 evidence integration 哪裡失效、調整 tool prompts 與 routing rules，然後重新執行整個 evaluation set。

## 7. 討論
程式碼維運代理的最大優勢在於，它把軟體維護視為 workflow 問題，而不是純粹的文字生成問題。透過明確的工具與 orchestration，系統可以減少無根據猜測，並為工程師提供一條可追蹤、可審查的診斷路徑。

但本設計也有其限制。系統品質仍依賴工具穩定性、repository context 的新鮮度，以及長期記憶的覆蓋率。另外，如果 schema 設計不佳或 escalation threshold 設太寬，依然可能產生過度自信的建議。這些風險可透過 read-only 預設、confidence gating、schema validation 與 human approval 來部分緩解。

未來可擴充方向包括加入 patch validation sandbox、整合更完整的 runbook retrieval，以及改善針對特定服務失敗模式的長期記憶索引。

## 8. 結論
本報告提出一個面向軟體維護工作的實用 AI Harness 設計。程式碼維運代理讓 LLM 擔任 controller，結合結構化工具、記憶層與混合式 orchestration，形成一個邏輯一致、可解釋且符合實務需求的系統。此設計符合本作業目標，因為它清楚展示了 AI 如何在不以模型訓練為主軸的前提下，透過 tool use、workflow control 與 decision-making 來完成複雜任務。
