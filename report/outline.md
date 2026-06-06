# Written Report Draft Outline (2-5 Pages)

## 1. Problem Definition and Background
- Application scenario: Code Operations Agent for software maintenance.
- Target users: on-call engineers, backend/frontend developers, and tech leads.
- Main pain points:
  - Slow triage of CI failures and production alerts.
  - Context switching across issue tracker, logs, and repository.
  - Inconsistent incident handling quality between engineers.
- Scope:
  - Focus on issue triage, root-cause hypothesis, and repair proposal.
  - Exclude direct deployment execution and force-push actions.
- Constraints:
  - Latency target: first actionable diagnosis within 90 seconds.
  - Cost target: bounded tool calls per task.
  - Safety: read-only by default, write actions require explicit approval.
  - Privacy: avoid exposing secrets in prompts and summaries.

## 2. AI Harness System Design
- LLM role: system controller that decides next action, invokes tools, and composes final output.
- Tool layer:
  - Tool A: Issue/PR Context Fetcher
  - Tool B: CI Log Analyzer
  - Tool C: Repo Code Search + Diff Planner
  - Tool D (optional): Runbook Retriever
- Memory layer:
  - Short-term task memory (current incident state, hypotheses, pending actions)
  - Long-term memory (resolved incidents, known fixes, service-specific patterns)
- Orchestration layer:
  - State-machine controller with deterministic transitions and guardrails.
- Data flow:
  - User request -> intent parse -> plan -> tool calls -> evidence merge -> recommendation.

## 3. Tool Design (At Least 3)
### Tool A: Issue/PR Context Fetcher
- Purpose: gather issue metadata, linked PRs, recent comments, and ownership.
- Input schema:
  - `repo: string`
  - `issue_or_pr_id: string`
  - `time_window_hours: integer`
- Output schema:
  - `title: string`
  - `status: string`
  - `participants: string[]`
  - `recent_events: object[]`
- Trigger condition:
  - User references incident ID, PR number, or bug ticket.
- Failure handling:
  - Retry once, then fall back to manual ID confirmation request.

### Tool B: CI Log Analyzer
- Purpose: parse failed job logs, summarize failure signature, and map to likely causes.
- Input schema:
  - `repo: string`
  - `workflow_run_id: string`
  - `job_id: string`
- Output schema:
  - `failure_signature: string`
  - `error_lines: string[]`
  - `likely_causes: string[]`
  - `confidence: number`
- Trigger condition:
  - Build/test/deploy pipeline failure in user request.
- Failure handling:
  - If logs unavailable, request alternate run ID and continue with partial analysis.

### Tool C: Repo Code Search + Diff Planner
- Purpose: locate suspicious code paths and propose minimal patch plan.
- Input schema:
  - `repo: string`
  - `query: string`
  - `branch: string`
- Output schema:
  - `candidate_files: string[]`
  - `suspect_functions: string[]`
  - `patch_plan: object[]`
- Trigger condition:
  - Root-cause hypothesis exists and code evidence is needed.
- Failure handling:
  - Use broader query strategy and return confidence downgrade.

## 4. Workflow / Agent Flow
- Stage 1: Intent understanding
  - Classify request: CI failure triage, bug diagnosis, regression analysis, or patch planning.
- Stage 2: Plan generation
  - Build ordered tool-call plan and stop conditions.
- Stage 3: Tool execution
  - Call Tool A -> Tool B -> Tool C depending on task class.
- Stage 4: Evidence integration
  - Merge cross-tool outputs, detect contradictions, request one extra tool call if needed.
- Stage 5: Final response
  - Return diagnosis, confidence, patch candidates, risk notes, and next actions.
- Branch case:
  - If CI logs show flaky test pattern, route to "stability remediation" branch.
  - If deterministic compile error, route to "direct patch proposal" branch.
- Error recovery:
  - Timeout -> retry with reduced scope.
  - Invalid schema -> auto-reformat request and retry once.
- Memory policy:
  - Persist incident signature, accepted fix, and postmortem tags.

## 5. AI Orchestration and Decision Logic
- Controller type: hybrid (state-machine + rule constraints + LLM planner).
- Decision checkpoints:
  - Checkpoint 1: is user request sufficiently scoped?
  - Checkpoint 2: do we have minimum evidence for diagnosis?
  - Checkpoint 3: is confidence high enough for patch recommendation?
- Stop conditions:
  - Evidence coverage threshold reached.
  - Max tool-call budget reached.
  - User asks for handoff.
- Escalation strategy:
  - Low confidence or conflicting evidence -> escalate to human reviewer with compact evidence pack.
- Observability:
  - Log each tool call, latency, token usage, retry count, and decision rationale.

## 6. Evaluation Method
- Metrics:
  - Task completion rate
  - Tool-call accuracy
  - Root-cause precision@1
  - Mean time to first actionable recommendation
  - Failure recovery success rate
- Test set:
  - 30 historical maintenance cases (CI failures, production bugs, regressions).
- Scoring:
  - 0-2 scale for diagnosis quality, actionability, and safety compliance.
- Baseline:
  - LLM-only assistant without tools.
- Optimization loop:
  - Weekly error analysis -> update routing rules -> refine tool prompts -> re-evaluate.

## 7. Conclusion
- Strengths:
  - Faster triage, stronger evidence grounding, and reproducible incident handling.
- Limitations:
  - Depends on tool reliability and repository metadata quality.
- Future improvements:
  - Add automated patch validation sandbox and deeper service-level memory retrieval.
