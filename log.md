# AI Harness 設計紀錄

## 專案資訊
- 開始日期：2026-05-21
- 作業類型：AI Harness system design
- 主題：Code Operations Agent（程式碼維運代理）

## 紀錄格式
每筆紀錄使用以下欄位：
- 時間：
- 提示／需求：
- AI 回應摘要：
- 設計決策：
- 發現問題：
- 修正／調整：
- 下一步：

---

## Entry 001
- 時間：2026-05-21
- 提示／需求：將原本的 DRL 作業工作區改成新的 AI Harness 作業規格。
- AI 回應摘要：將原本以 DRL 為主的 instruction 與 TODO 結構改寫為 AI Harness 版本。
- 設計決策：將專案主軸從演算法 survey 轉為 system orchestration design。
- 發現問題：原有檔案內容完全對應舊題目，已不符合新的評分方向。
- 修正／調整：重寫 `instruction.md` 與 `todo.md`，並建立 `log.md`。
- 下一步：選定一個應用場景並開始架構草稿。

## Entry 002
- 時間：2026-05-27
- 提示／需求：確認主題選擇為「Code Operations Agent」。
- AI 回應摘要：將規劃檔案改為軟體維護型 AI Harness 設計。
- 設計決策：
  - 選擇以 CI triage、錯誤診斷與 patch planning 為核心的程式碼維運場景。
  - 採用 hybrid orchestration（state-machine + LLM controller）。
  - 定義三個核心工具與 schema-driven function calling。
- 發現問題：
  - 既有模板仍過於通用，尚未綁定特定應用場景。
- 修正／調整：
  - 更新 `todo.md` 的 Step 0-6 進度。
  - 填寫 `report/outline.md` 的場景化內容。
  - 重寫 `figures/infographic_plan.md` 的版面與流程。
  - 新增 `notes/code_ops_agent_design.md` 作為架構與評估筆記。
- 下一步：
  - 依大綱撰寫 2-5 頁正式報告。
  - 依資訊圖規劃製作圖稿。

## Entry 003
- 時間：2026-06-03
- 提示／需求：撰寫書面報告初稿。
- AI 回應摘要：將大綱擴寫成 Code Operations Agent 的完整報告初稿。
- 設計決策：
  - 報告重點放在 system design、tool orchestration 與 workflow control。
  - 章節結構直接對齊作業評分項目。
  - 為了安全性，將 deploy 與 merge 類動作排除在系統範圍外。
- 發現問題：
  - 專案雖然已有設計筆記與大綱，但尚未有可提交的報告正文。
- 修正／調整：
  - 新增 `report/report.md`。
  - 同步更新 `todo.md`，標記報告初稿相關項目已完成。
- 下一步：
  - 做最後的文字潤稿與頁數控制。
  - 將資訊圖規劃轉成最終圖稿內容。

## Entry 004
- 時間：2026-06-03
- 提示／需求：潤飾英文初稿、製作中文版本，並完成資訊圖最終文字稿。
- AI 回應摘要：新增較正式的英文版報告、中文版報告，以及資訊圖最終文案檔。
- 設計決策：
  - 保留原始英文初稿，另做一份更正式的英文版。
  - 中文版不採逐句直譯，而是以可直接交件為目標重寫。
  - 將資訊圖規劃改寫為 panel-by-panel 的最終內容，方便排版。
- 發現問題：
  - 專案已有不錯的初稿與規劃，但仍缺少更接近最終展示用途的文字包。
- 修正／調整：
  - 新增 `report/report_polished.md`。
  - 新增 `report/report_zh.md`。
  - 新增 `figures/infographic_final.md`。
  - 更新 `todo.md`，反映資訊圖內容已具備。
- 下一步：
  - 針對選定語言版本做頁數壓縮。
  - 將資訊圖文案真正排成圖。

## Entry 005
- 時間：2026-06-06
- 提示／需求：完成最後三項收尾工作，包括精簡中文版、單頁資訊圖文案與 submission checklist。
- AI 回應摘要：產出較短的中文終稿、一頁式中文資訊圖文案，以及獨立的 final submission checklist。
- 設計決策：
  - 額外保留一份精簡中文版，作為最適合提交的版本。
  - 將資訊圖內容整理成 presentation-ready blocks，而不只是規劃筆記。
  - 增加一份獨立 checklist，讓最後交件整理更明確。
- 發現問題：
  - 專案內容雖完整，但最後交件相關檔案仍分散在不同資料夾。
- 修正／調整：
  - 新增 `report/report_zh_final.md`。
  - 新增 `figures/infographic_onepage_zh.md`。
  - 新增 `notes/submission_checklist.md`。
  - 更新 `todo.md`，標記校稿、資訊圖文案與 log 品質檢查已完成。
- 下一步：
  - 若課程有嚴格命名規則，需再調整檔名。
  - 若老師要求非 Markdown 格式，需再匯出成最終格式。

## Entry 006
- 時間：2026-06-06
- 提示／需求：將最終交件內容整理到 `summition` 資料夾。
- AI 回應摘要：把最終報告、資訊圖文案與 log 集中成一個交件包。
- 設計決策：
  - 以精簡中文版報告作為主要報告交件版本。
  - 以單頁中文資訊圖文案作為資訊圖交件文字稿。
  - 保留使用者指定的資料夾拼法：`summition`。
- 發現問題：
  - 最終交件檔案原本散落在不同目錄，交付時不夠直觀。
- 修正／調整：
  - 建立 `summition/`。
  - 將三個主要交件檔複製進去，並加上排序檔名。
  - 新增 `summition/README.md` 說明交件包內容。
- 下一步：
  - 若課程有指定檔名規則，再進一步重新命名。
  - 若需要 PDF 或圖片格式，再進行匯出或轉檔。

## Entry 007
- 時間：2026-06-06
- 提示／需求：重新檢查資訊圖內容是否符合原始作業要求，修正內容後直接產出圖檔。
- AI 回應摘要：重寫資訊圖文案結構，刪除過度分散注意力的內容，並產出一份可直接提交的 SVG 資訊圖。
- 設計決策：
  - 讓資訊圖聚焦在四個作業要求：architecture、workflow、function calling、sequence/pipeline。
  - 把 problem statement 與過重的敘述性內容降到最低，避免搶走核心系統設計版面。
  - 以 SVG 形式產出，方便本地直接提交或後續匯出。
- 發現問題：
  - 舊版資訊圖文案雖然方向正確，但版面焦點分散，對作業要求的對應不夠直接。
  - 交件資料夾中原本只有資訊圖文字稿，沒有真正的圖檔。
- 修正／調整：
  - 重寫 `figures/infographic_final.md`。
  - 重寫 `figures/infographic_onepage_zh.md`。
  - 新增 `figures/code_ops_agent_infographic.svg`。
  - 複製圖檔到 `summition/02_infographic.svg`。
  - 更新 `summition/README.md`。
- 下一步：
  - 若老師要求 PNG 或 PDF，再從 SVG 匯出對應格式。

## Entry 008
- 時間：2026-06-07
- 提示／需求：將目前整理好的內容直接轉成 PDF。
- AI 回應摘要：將第一部分與第三部分的合併預覽檔轉成 PDF，並將資訊圖 SVG 轉成 PDF。
- 設計決策：
  - 使用本機 Chrome 的 headless print-to-pdf 功能，而不是額外安裝轉檔套件。
  - 先將 Markdown 轉為本地 HTML，再輸出成 PDF。
  - 資訊圖部分直接由 SVG 轉成 PDF，以保留版面與向量清晰度。
- 發現問題：
  - 在沙箱內直接啟動瀏覽器無法成功落檔，需要額外權限。
  - 原本透過 HTML wrapper 輸出的資訊圖 PDF 沒有成功，因此改用直接列印 SVG。
- 修正／調整：
  - 新增 `notes/render_submission.py` 生成 HTML 中介檔。
  - 產出 `summition/part1_part3_preview.pdf`。
  - 產出 `summition/02_infographic.pdf`。
  - 更新 `summition/README.md`。
- 下一步：
  - 若老師要求正式檔名，再依規則重新命名 PDF。

