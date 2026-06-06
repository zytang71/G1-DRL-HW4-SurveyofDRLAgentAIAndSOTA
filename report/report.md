# Code Operations Agent: An AI Harness for Software Maintenance

## Abstract
This report proposes an AI Harness system for software maintenance, named the Code Operations Agent. The system is designed for operational tasks such as CI failure triage, bug diagnosis, regression analysis, and safe patch planning. The design focus is not model training. Instead, the focus is how a large language model acts as a system controller that coordinates multiple tools, uses memory, and follows a multi-step workflow to solve complex engineering tasks. The proposed system includes three core tools, a hybrid orchestration mechanism, a structured function-calling policy, and an evaluation plan based on historical maintenance cases. The goal is to reduce triage time, improve evidence grounding, and make incident handling more consistent across engineers.

## 1. Problem Definition and Application Background
Modern software teams spend significant time diagnosing CI failures, investigating regressions, and collecting fragmented evidence from issue trackers, logs, and source repositories. In many cases, the hardest part is not writing the final patch, but identifying the most likely cause and deciding what to inspect next. This work is usually repetitive, context-heavy, and dependent on individual engineer experience.

The proposed application scenario is a Code Operations Agent for software maintenance. The target users are on-call engineers, backend and frontend developers, and technical leads who need fast and evidence-based support during debugging and incident triage. The system is intended to help them understand a failure, collect relevant context, and propose a minimal repair direction.

The problem scope is intentionally limited. The agent supports issue triage, root-cause hypothesis generation, and patch planning, but it does not directly deploy code, merge pull requests, or execute destructive repository actions. This boundary is important for safety and explainability. The system should produce a first actionable diagnosis within 90 seconds, keep tool usage bounded to control cost, and avoid exposing secrets in prompts or summaries.

## 2. AI Harness System Architecture
The Code Operations Agent is designed as an AI Harness with four major layers: the LLM controller, the tool layer, the memory layer, and the orchestration layer.

The LLM controller is the central decision-maker. It interprets the user request, decides which tools are needed, evaluates intermediate evidence, and produces the final response. The LLM is not treated as a standalone chatbot. It acts as a structured system controller responsible for planning and coordination.

The tool layer provides external capabilities that the LLM cannot reliably perform by itself. In this design, the system includes three mandatory tools and one optional tool. Tool A, Issue/PR Context Fetcher, retrieves issue metadata, linked pull requests, ownership information, and recent discussion events. Tool B, CI Log Analyzer, extracts failure signatures and likely causes from workflow logs. Tool C, Repo Code Search plus Diff Planner, finds relevant code paths and proposes a minimal patch plan. An optional Tool D, Runbook Retriever, can be added later to fetch operational procedures or service-specific troubleshooting guides.

The memory layer contains short-term and long-term memory. Short-term memory stores the current case state, such as the incident identifier, current hypotheses, completed tool calls, unresolved questions, and confidence level. Long-term memory stores recurring incident signatures, validated fixes, and service-specific repair patterns. This separation allows the agent to remain grounded in the current task while benefiting from previous operational experience.

The orchestration layer controls the workflow. It uses a hybrid design: deterministic state transitions enforce guardrails, while the LLM planner handles task-specific reasoning inside each state. The main data flow is: user request to intent parsing, then plan generation, then tool execution, then evidence integration, and finally recommendation output. This architecture makes control flow explicit and easier to evaluate than a purely free-form agent loop.

## 3. Function Calling and Tool Usage Design
Function calling is the core mechanism that converts user intent into system action. The agent does not call tools blindly. Each tool has a defined purpose, schema, trigger condition, and fallback behavior.

Tool A, Issue/PR Context Fetcher, is used when the request references an incident ticket, bug report, or pull request. Its input includes a repository name, an issue or PR identifier, and a time window. Its output contains title, status, participants, and recent events. This tool gives the controller operational context before deeper diagnosis begins. If the identifier is invalid or missing, the system retries once and then asks for a narrower reference.

Tool B, CI Log Analyzer, is triggered when the request involves a failed build, test, or deployment pipeline. Its input includes the repository, workflow run identifier, and job identifier. It returns a failure signature, important error lines, likely causes, and a confidence score. This tool reduces the need for the LLM to inspect raw logs directly and helps normalize noisy failures into a compact diagnostic summary.

Tool C, Repo Code Search plus Diff Planner, is used after an initial hypothesis exists and the controller needs code evidence. It accepts a repository, query string, and branch, then returns candidate files, suspect functions, and a patch plan. Its goal is not to write a final patch automatically, but to narrow investigation to the smallest plausible code area and propose a repair direction.

All tool outputs are schema-validated before they are accepted by the controller. If a tool times out, the controller retries once with narrower scope. If the tool returns malformed output, the system requests normalized output and retries once. Write actions remain disabled by default, which ensures the agent remains advisory rather than autonomous in high-risk repository operations.

## 4. Multi-step Agent Workflow
The workflow begins with intent understanding. The LLM controller classifies the request into categories such as CI failure triage, runtime bug diagnosis, regression analysis, or patch planning. This classification determines the initial tool-call plan.

Next, the system enters the planning stage. The controller creates an ordered plan with a tool-call budget, expected evidence targets, and stop conditions. This step is important because it prevents unnecessary tool usage and makes the workflow inspectable.

During tool execution, the controller calls the tools in an order appropriate to the task. A typical CI incident would first use Tool A for contextual metadata, then Tool B for failure signature analysis, and finally Tool C for code localization and patch planning. Not every task requires all tools. The workflow is conditional rather than fixed.

After tool execution, the evidence integration stage merges outputs from different tools. The controller compares signals across issue context, logs, and source code. If the evidence is consistent, the agent builds a final diagnosis. If the evidence conflicts, the controller may perform one additional tool call or lower its confidence.

The final response generation stage returns a structured result: likely root cause, confidence score, candidate files or functions, repair proposal, risk notes, and recommended next steps for the engineer.

The workflow also includes branching and recovery logic. If the CI logs suggest a flaky test pattern, the controller routes to a stability remediation branch rather than a direct patch branch. If the error is a deterministic compilation failure, the system routes to a direct patch proposal branch. For timeouts or invalid tool output, the controller retries with reduced scope. After each completed case, the system updates memory with the final incident signature, accepted fix, and postmortem tags.

## 5. AI Orchestration and Decision Logic
The orchestration strategy is hybrid. A state-machine enforces the allowed flow between request intake, planning, tool execution, evidence integration, and response generation. Within each state, the LLM performs reasoning and decision support. This approach balances flexibility with control.

Three decision checkpoints are used. First, the system checks whether the user request is sufficiently scoped. Second, it checks whether the minimum required evidence has been collected. Third, it checks whether the confidence level is high enough to present a patch recommendation instead of only a hypothesis.

The controller also defines explicit stop conditions. The workflow ends when evidence coverage is sufficient, when the tool-call budget is exhausted, or when the user requests human handoff. If confidence remains low or evidence is contradictory, the system escalates to a human reviewer. Instead of hiding uncertainty, it provides a compact evidence pack containing retrieved context, failure signature, conflicting clues, and recommended next inspection steps.

Observability is part of the design. Each tool call, retry count, latency measurement, token usage, and controller decision should be logged. This supports both debugging and later evaluation of the harness behavior.

## 6. Evaluation Method
The proposed evaluation uses an offline case set of 30 historical maintenance incidents covering CI failures, regressions, and runtime bugs. Each case contains enough repository, issue, and log context to simulate realistic operational tasks.

Five evaluation dimensions are used. The first is task completion rate, which measures whether the system produces a usable diagnostic result. The second is tool-call accuracy, which measures whether the chosen tools match the information need of the task. The third is root-cause precision at one, which evaluates whether the top-ranked hypothesis is correct. The fourth is mean time to first actionable recommendation, which reflects operational usefulness. The fifth is failure recovery success rate, which evaluates whether the system remains useful when tools time out or return incomplete results.

Scoring can use a 0 to 2 scale on diagnosis quality, actionability, and safety compliance. A score of 0 means incorrect or unsafe output, 1 means partially correct or weakly actionable output, and 2 means correct, evidence-based, and operationally useful output.

The baseline system is an LLM-only assistant with no tool access. Comparing the harness against this baseline highlights the value of structured tool use and workflow control. The optimization loop is straightforward: review weekly failures, inspect where routing or evidence integration broke down, refine tool prompts and routing rules, and re-run the evaluation set.

## 7. Conclusion
This report presents a practical AI Harness design for software maintenance. The Code Operations Agent uses an LLM as a controller, combines it with specialized tools and memory, and constrains the process through hybrid orchestration. The design addresses a realistic engineering problem where evidence collection and workflow control matter more than raw text generation.

The main strengths of the design are faster triage, stronger evidence grounding, and more consistent incident handling. The main limitations are dependence on tool reliability, possible stale repository context, and the risk of overconfident diagnosis. Future improvements include adding a patch-validation sandbox, deeper runbook retrieval, and better long-term memory for service-specific failures. Even in its current form, the proposed system satisfies the assignment goal by clearly showing how AI performs tool use, decision-making, and workflow orchestration in a logically consistent way.
