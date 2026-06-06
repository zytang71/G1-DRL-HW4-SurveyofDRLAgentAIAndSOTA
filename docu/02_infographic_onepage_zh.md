# 程式碼維運代理：單頁資訊圖文案

## 主標題
程式碼維運代理：軟體維護用 AI Harness

## 副標題
以 LLM 為控制器，整合工具、記憶與 workflow，支援 CI 排查、錯誤診斷與修補規劃

## 區塊 1：問題背景
標題：
- 為什麼軟體維護很慢？

文案：
- 工程師需要反覆切換 issue、logs 與 source code。
- 相似 incident 往往被不同人用不同方式處理。
- 真正耗時的常是 root-cause analysis，而不是最後修改程式碼。

## 區塊 2：系統目標
標題：
- 這個代理要做什麼？

文案：
- 快速診斷 CI failures 與 regressions。
- 在回答前先蒐集工具證據。
- 提出安全、最小化且可解釋的修補方向。

## 區塊 3：整體架構
標題：
- AI Harness Architecture

節點：
- User Request
- LLM Controller
- Orchestration State Machine
- Tool A: Issue/PR Context Fetcher
- Tool B: CI Log Analyzer
- Tool C: Repo Code Search + Diff Planner
- Short-term Memory
- Long-term Memory
- Final Recommendation

箭頭標籤：
- request
- classify
- plan
- call tool
- retrieve context
- analyze logs
- localize code
- store case state
- retrieve prior fixes
- synthesize response

圖說：
- LLM 負責控制流程，tools 提供證據，memory 保留上下文。

## 區塊 4：Function Calling Flow
標題：
- Tool Chain

步驟：
1. 接收 incident ID 或 CI failure 描述。
2. 分類任務類型並建立 tool plan。
3. 抓取 issue 與 PR context。
4. 解析 CI logs 並抽取 failure signature。
5. 搜尋 repository 並提出 patch direction。
6. 整合證據並計算 confidence。
7. 輸出 diagnosis、risks 與 next actions。

補充標語：
- 所有 tool outputs 都要通過 schema validation。
- Timeout 或 malformed output 只允許一次受控重試。

## 區塊 5：Workflow Branches
標題：
- Decision Branches

分支 A：
- 若 logs 顯示 flaky tests
- 轉入 stability remediation branch

分支 B：
- 若 logs 顯示 deterministic compile failure
- 直接進入 patch planning branch

分支 C：
- 若證據衝突或 confidence 過低
- 升級給 human reviewer，附上 evidence pack

## 區塊 6：Memory Layer
標題：
- Memory Design

短期記憶：
- Incident ID
- Current hypothesis
- Completed tool calls
- Open questions
- Confidence score

長期記憶：
- Recurring failure signatures
- Known fixes
- Service-specific repair patterns

## 區塊 7：Safety Guardrails
標題：
- Guardrails

文案：
- Read-only by default
- No auto-merge
- No auto-deploy
- Confidence gating before patch recommendation
- Human approval for risky actions
- Evidence-based claims only

## 區塊 8：Evaluation
標題：
- How is the system evaluated?

文案：
- 30 historical maintenance incidents
- Metrics:
  - task completion rate
  - tool-call accuracy
  - root-cause precision@1
  - time to first actionable recommendation
  - failure recovery success rate
- Baseline:
  - LLM-only assistant without tools

## 區塊 9：Final Output
標題：
- Final Response Format

文案：
- Likely root cause
- Confidence score
- Relevant files/functions
- Patch plan
- Risk notes
- Next recommended actions

## 建議版面
- 上排：標題、副標題、問題背景、系統目標
- 中排：整體架構圖、tool chain
- 下排：workflow branches、memory、guardrails
- 底排：evaluation、final output

## 建議配色
- 藍色：controller 與 orchestration
- 橘色：tools
- 綠色：memory
- 紅色：risk 與 escalation
- 灰色：user input 與 final output
