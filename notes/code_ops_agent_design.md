# Code Operations Agent - System Design Notes

## Scenario Statement
- Build an AI Harness that assists software maintenance tasks.
- Main tasks:
  - CI failure triage
  - bug root-cause hypothesis
  - patch planning support

## Architecture
- Controller:
  - LLM receives request, plans tool calls, and composes final answer.
- Orchestration:
  - State-machine with deterministic transitions.
- Tool layer:
  - Tool A: Issue/PR Context Fetcher
  - Tool B: CI Log Analyzer
  - Tool C: Repo Code Search + Diff Planner
- Memory:
  - Short-term memory: per-incident context.
  - Long-term memory: recurring incident signatures and validated fixes.

## Function Calling Policy
- Tool invocation only when criteria are met.
- All tool outputs must pass schema checks.
- Retry rules:
  - timeout -> one retry with narrowed scope
  - malformed output -> normalize and retry once
- Write actions disabled by default.

## Workflow
1. Parse intent and classify request type.
2. Build tool-call plan with budget.
3. Execute tools in planned order.
4. Merge evidence and compute confidence.
5. Branch:
   - low confidence -> escalation package for human review
   - high confidence -> patch proposal and action checklist
6. Update memory with incident signature and outcome.

## Evaluation Plan
- Offline evaluation set:
  - 30 historical incidents
  - balanced across CI, regression, and runtime bugs
- Metrics:
  - completion rate
  - root-cause precision@1
  - recommendation actionability
  - time to first actionable output
  - tool-call failure recovery rate
- Baseline:
  - same LLM without tool calls

## Risks and Guardrails
- Risks:
  - hallucinated causes
  - stale code context
  - overconfident recommendations
- Guardrails:
  - evidence citation required per claim
  - confidence threshold gating
  - human approval before merge/deploy advice
