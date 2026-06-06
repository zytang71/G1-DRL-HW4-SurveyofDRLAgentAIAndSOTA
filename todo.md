# AI Harness Homework TODO

## 0. Setup and Scope
- [ ] Confirm team member names / student IDs.
- [x] Decide report style: A4 or IEEE (current default: IEEE-like).
- [x] Confirm workspace folders exist:
  - [x] `report/`
  - [x] `figures/`
  - [x] `notes/`
- [x] Create mandatory process log file: `log.md`.
- [x] Choose one application scenario:
  - [ ] Search assistant
  - [ ] Customer service system
  - [ ] Data analysis agent
  - [ ] Education assistant
  - [x] Other scenario: Code Operations Agent (software maintenance assistant)

## 1. Problem Definition
- [x] Define target users.
- [x] Define core user pain points.
- [x] Define concrete task scope and boundaries.
- [x] Define success criteria for the system.
- [x] Write constraints (latency, cost, safety, privacy).

## 2. AI Harness Architecture
- [x] Design full architecture:
  - [x] LLM as system controller
  - [x] Tool layer
  - [x] Memory layer
  - [x] Orchestration/controller layer
- [x] Draw architecture diagram for report and infographic.
- [x] Define data flow between user, LLM, tools, and memory.
- [x] Specify where decisions are made and how tool routing works.

## 3. Function Calling and Tool Usage
- [x] Define at least 3 tools (API/function):
  - [x] Tool A: Issue/PR Context Fetcher
  - [x] Tool B: CI Log Analyzer
  - [x] Tool C: Repo Code Search + Diff Planner
- [x] For each tool, document:
  - [x] Purpose
  - [x] Input schema
  - [x] Output schema
  - [x] Failure modes
  - [x] Retry/fallback strategy
- [x] Explain function calling trigger rules.
- [x] Explain tool selection policy and guardrails.

## 4. Agent Workflow (Multi-step)
- [x] Design end-to-end multi-step workflow.
- [x] Define each stage:
  - [x] Intent understanding
  - [x] Planning
  - [x] Tool calling
  - [x] Result integration
  - [x] Final response generation
- [x] Add at least 1 branch case (conditional decision path).
- [x] Add error-handling path (tool timeout/invalid output).
- [x] Add memory update policy after each step.

## 5. AI Orchestration and Decision Logic
- [x] Describe orchestration mechanism:
  - [ ] Rule-based controller
  - [ ] Graph/state-machine style
  - [x] Hybrid approach
- [x] Define decision checkpoints and stop conditions.
- [x] Define escalation strategy for uncertain cases.
- [x] Define observability/logging points.

## 6. Evaluation Design
- [x] Define evaluation dimensions:
  - [x] Task completion rate
  - [x] Tool-call accuracy
  - [x] Response quality/consistency
  - [x] Latency
  - [x] Failure recovery quality
- [x] Prepare evaluation dataset/case set.
- [x] Create scoring rubric and pass criteria.
- [x] Define baseline system for comparison.
- [x] Propose optimization loop from evaluation findings.

## 7. Deliverable 1 - Written Report (Required)
- [x] Target length 2-5 pages (A4/IEEE).
- [x] Include:
  - [x] Problem definition and background
  - [x] AI Harness architecture
  - [x] Tool design (>=3 tools)
  - [x] Workflow/agent flow
  - [x] Evaluation method
- [x] Add logical consistency review.
- [x] Add final proofreading.

## 8. Deliverable 2 - Infographic (Required)
- [x] Include architecture view (LLM/tools/memory).
- [x] Include orchestration/workflow flow.
- [x] Include function-calling/tool-chain flow.
- [x] Add one sequence diagram or pipeline visualization.
- [x] Ensure labels are readable and consistent.

## 9. Deliverable 3 - log.md (Required)
- [x] Record prompt/chat history with AI.
- [x] Record iteration history.
- [x] Record architecture changes and design decisions.
- [x] Record issue analysis and fixes.
- [x] Keep logs chronological with timestamps.

## 10. Rubric Alignment Self-check
- [x] AI system design completeness (35%).
- [x] Tool/orchestration design (25%).
- [x] Workflow logic clarity (20%).
- [x] Infographic clarity (10%).
- [x] log.md process record quality (10%).

## 11. Final Submission Checklist
- [x] All three required deliverables are complete.
- [x] Tool usage and decision-making are clearly explained.
- [x] Design is logically consistent and explainable.
- [x] System-design focus is clear (not model training focus).
- [ ] File naming and format match course rules.
