# Code Operations Agent: An AI Harness for Software Maintenance

## Abstract
This report presents the design of a Code Operations Agent, an AI Harness system for software maintenance. The system is intended to support operational engineering tasks such as CI failure triage, regression diagnosis, bug investigation, and repair planning. The emphasis of the design is not model training, but system orchestration: a large language model acts as the controller, invokes external tools through structured function calling, uses task memory, and follows a multi-step workflow to produce evidence-based recommendations. The proposed harness includes three core tools, a hybrid orchestration strategy, clear safety boundaries, and an offline evaluation plan. The design goal is to shorten incident triage time, improve diagnostic consistency, and make the reasoning process more explainable to engineers.

## 1. Problem Definition and Background
Software maintenance work is often slowed by fragmented evidence. When a build fails or a regression appears, engineers typically need to inspect issue trackers, CI logs, pull requests, source files, and historical fixes before they can form a reliable diagnosis. This process is time-consuming and highly dependent on personal experience. As a result, similar incidents may be handled with very different quality and speed by different engineers.

The proposed application is a Code Operations Agent for software maintenance. The target users are on-call engineers, software developers, and technical leads who need fast support during triage and debugging. The agent is designed to help users collect relevant context, prioritize the next diagnostic action, and generate a safe repair proposal supported by evidence.

The system scope is intentionally constrained. The agent focuses on triage, diagnosis, and patch planning. It does not automatically merge pull requests, deploy services, or execute destructive repository actions. This boundary is necessary because software operations are safety-sensitive. The system must remain explainable, bounded in cost, and operationally safe. In this design, the target is to return a first actionable diagnosis within 90 seconds while limiting unnecessary tool calls and preventing sensitive information leakage in prompts or summaries.

## 2. AI Harness Architecture
The Code Operations Agent is structured as an AI Harness with four coordinated layers: the LLM controller, the tool layer, the memory layer, and the orchestration layer.

The LLM controller is the central component of the system. It receives the user request, interprets the operational intent, selects the next action, decides whether a tool call is necessary, and synthesizes the final response. In other words, the model is not used as a general chatbot but as a controlled decision-maker within a larger system.

The tool layer provides access to external information sources and task-specific utilities. In the current design, the system contains three core tools. The first is the Issue/PR Context Fetcher, which gathers issue metadata, linked pull requests, ownership information, and recent comments. The second is the CI Log Analyzer, which extracts failure signatures and probable causes from workflow logs. The third is the Repo Code Search plus Diff Planner, which searches relevant code paths and proposes a minimal patch plan. An optional fourth tool, a Runbook Retriever, may be added to retrieve standard operating procedures or service-specific troubleshooting guides.

The memory layer contains both short-term and long-term memory. Short-term memory stores case-local information such as the incident identifier, current hypothesis, completed tool calls, unresolved questions, and confidence score. Long-term memory stores recurring failure patterns, known fixes, and service-specific operational knowledge. This separation supports both immediate task continuity and gradual system improvement over time.

The orchestration layer governs the workflow. It is responsible for state transitions, stop conditions, guardrails, and escalation behavior. The overall data flow is straightforward: the user submits a request, the controller classifies the request, generates a tool plan, calls tools, integrates evidence, and returns a recommendation. This explicit structure makes the system easier to debug and evaluate than a free-form autonomous loop.

## 3. Function Calling and Tool Usage
Function calling is the mechanism that allows the LLM controller to transform intent into concrete system action. Each tool is defined with a clear purpose, input schema, output schema, activation condition, and fallback path.

The Issue/PR Context Fetcher is used when the user references a bug ticket, incident ID, or pull request. Its input includes a repository name, an issue or PR identifier, and a time window. Its output includes title, status, participants, and recent events. This tool gives the controller immediate operational context before deeper diagnosis begins.

The CI Log Analyzer is triggered when the task involves a failed build, failed test, or deployment error. Its input includes the repository, workflow run ID, and job ID. Its output contains a failure signature, important error lines, likely causes, and a confidence score. The purpose of this tool is to compress noisy logs into a structured diagnostic signal.

The Repo Code Search plus Diff Planner is activated after a likely cause has been identified and the controller needs source-level evidence. Its input includes the repository, branch, and search query. Its output contains candidate files, suspect functions, and a patch plan. The tool is designed to reduce the search space for engineers rather than to replace engineering judgment.

All tool outputs are schema-validated. If a tool times out, the controller retries once with narrower scope. If output is malformed, the controller requests normalization and retries once. The system is read-only by default. Any recommendation related to code modification remains advisory until a human engineer reviews it. This policy limits the operational risk of tool misuse.

## 4. Multi-step Agent Workflow
The proposed workflow contains five main stages.

The first stage is intent understanding. The controller classifies the incoming request into categories such as CI failure triage, regression diagnosis, runtime bug investigation, or patch planning. This classification determines which evidence is needed and which tools are likely to be useful.

The second stage is planning. The controller prepares an ordered tool-call plan, defines a tool budget, and sets stop conditions. This stage prevents uncontrolled exploration and makes the harness behavior auditable.

The third stage is tool execution. For a typical CI incident, the controller first calls the Issue/PR Context Fetcher to gather background information, then the CI Log Analyzer to identify the failure signature, and finally the Repo Code Search plus Diff Planner to locate relevant code paths and propose a repair direction. Other incident types may use a shorter or different sequence.

The fourth stage is evidence integration. The controller compares information from issues, logs, and repository evidence. If the outputs agree, the controller forms a high-confidence diagnosis. If they conflict, it can request one additional tool call, reduce confidence, or escalate the case.

The fifth stage is final response generation. The output should include the likely root cause, the confidence score, the most relevant files or functions, the proposed fix direction, and any important risk notes.

The workflow also contains explicit branches. If the logs indicate a flaky or nondeterministic failure, the controller routes the case into a stability branch rather than a direct repair branch. If the logs indicate a deterministic compile or dependency error, the controller routes directly toward patch planning. Recovery logic is also defined: timeouts trigger a narrower retry, malformed tool output triggers schema repair, and unresolved conflicts trigger escalation. At the end of the process, the system stores the incident signature and accepted resolution into memory.

## 5. Orchestration and Decision Logic
The orchestration mechanism is hybrid. Deterministic state-machine constraints define what transitions are legal, while the LLM performs context-sensitive reasoning inside each state. This design combines control with flexibility.

Three decision checkpoints are central to the system. First, the controller checks whether the user request contains enough scope to act safely. Second, it checks whether enough evidence has been collected to justify a diagnosis. Third, it checks whether confidence is high enough to provide a repair proposal instead of a tentative hypothesis.

The system also defines clear stop conditions. The workflow stops when evidence coverage is sufficient, when the tool budget is exhausted, or when the user requests a human handoff. If evidence conflicts or confidence remains low, the controller escalates the task to a human engineer. Instead of giving a vague answer, it produces an evidence package containing the retrieved context, dominant failure signal, conflicting clues, and recommended next inspection steps.

Observability is treated as a required capability. The system records tool calls, latency, retry counts, token consumption, and controller decisions. These logs support later debugging, evaluation, and optimization of the harness.

## 6. Evaluation Method
The evaluation plan uses an offline dataset of 30 historical maintenance incidents. These cases should include CI failures, runtime bugs, and regressions, with balanced representation across incident types. Each case includes sufficient repository context, issue metadata, and logs to replay the decision process.

The primary evaluation metrics are task completion rate, tool-call accuracy, root-cause precision at one, mean time to first actionable recommendation, and failure recovery success rate. Together, these metrics assess not only correctness but also operational usefulness.

Scoring can be performed on a 0-2 scale across three dimensions: diagnosis quality, actionability, and safety compliance. A score of 0 indicates incorrect or unsafe behavior. A score of 1 indicates partially correct or weakly actionable output. A score of 2 indicates correct, evidence-grounded, and operationally useful output.

The baseline is an LLM-only assistant without tool access. This comparison is important because the assignment emphasizes orchestration and tool use. If the harness outperforms the baseline on precision, actionability, and recovery robustness, then the value of structured orchestration is demonstrated clearly.

The optimization loop follows a standard engineering process. Failed or low-scoring cases are reviewed weekly, routing rules are adjusted, tool prompts are refined, and the evaluation set is re-run. In this way, the harness improves through system-level iteration rather than retraining the model.

## 7. Discussion
The main strength of the Code Operations Agent is that it treats software maintenance as a workflow problem instead of a pure text-generation problem. By grounding the controller in tools and explicit orchestration, the system reduces unsupported guesses and gives engineers a traceable path from incident report to repair proposal.

The design also has limitations. Its quality depends on tool reliability, the freshness of repository context, and the coverage of historical memory. In addition, poor schema design or weak escalation thresholds could still allow overconfident recommendations. These risks are partially mitigated by read-only defaults, confidence gating, schema validation, and human approval before any action affecting code or deployment.

Future work could add a validation sandbox that tests proposed patches, a stronger runbook retrieval component, and better long-term memory indexing for service-specific failures.

## 8. Conclusion
This report proposes a practical AI Harness for software maintenance. The Code Operations Agent uses an LLM as a controller, combines it with structured tools and memory, and constrains the workflow through hybrid orchestration. The result is a system design that is logically consistent, explainable, and directly aligned with real engineering maintenance tasks. The design satisfies the assignment objective by showing how tool use, workflow control, and decision-making can be organized into a coherent AI system without relying on model training as the core contribution.
