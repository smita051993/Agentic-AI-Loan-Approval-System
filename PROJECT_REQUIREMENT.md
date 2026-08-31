Project Requirement — Agentic AI Intelligent Loan Approval System

> **Purpose:** This file is the single source of truth for Claude Code
> when working on this project. Read this file first, then inspect the
> existing repository before making any change. The project is already
> implemented. Do **not** rebuild or redesign it from scratch.

1. Project Identity

Project: Agentic AI Intelligent Loan Approval System
Repository:
https://github.com/smita051993/Agentic-AI-Loan-Approval-System/tree/master

The project is a multi-agent Agentic AI loan approval system based on
the supplied case study.

Primary goal

Analyze a loan application using specialized AI agents and produce:

• APPROVE
• REJECT
• REVIEW

The result must be explainable and auditable.

────────

2. Original Case-Study Requirements

Problem

Loan approval requires evaluating:

• applicant details
• credit history
• financial risk indicators
• regulatory/compliance rules

The target solution is a Multi-Agent Agentic AI system that analyzes
applications and classifies them as Approved, Rejected, or Requires
Manual Review.

Business objectives

1. Automate loan application analysis using Agentic AI.
2. Improve decision speed and consistency.
3. Provide explainable and auditable decisions.
4. Use a scalable, loosely coupled architecture.

Required input

• Applicant ID
• Applicant Profile:
  • Age
  • Income
  • Employment Type
• Credit Score
• Loan Amount
• Loan Tenure
• Existing Liabilities
• Location
• Application Timestamp

────────

3. Required Architecture

The case study requires these layers:

Presentation layer

• Streamlit-based loan application UI/chatbot-style interface.
• Submit loan data.
• Display final status and analysis.

Microservice layer

• FastAPI REST API.
• Receive and validate application data.

Orchestration layer

• LangGraph.
• Agent workflow coordination.
• Decision routing/state management.

Agent layer

Four domain-specific agents:

1. Applicant Profile Agent
2. Financial Risk Analysis Agent
3. Loan Decision Agent
4. Compliance & Action Orchestrator Agent

Communication layer

• MCP (Model Context Protocol).
• MCP servers provide tools/data to agents.

────────

4. Required Agent Responsibilities

Agent 1 — Applicant Profile Agent

MCP: ApplicantDB

Must analyze/return:

• Income Stability Score
• Employment Risk
• Credit History Summary
• Application Completeness Flags

Current implementation: agents/applicant_agent.py

────────

Agent 2 — Financial Risk Analysis Agent

MCP: RiskRulesDB

Must analyze/return:

• Debt-to-Income Ratio
• Credit Score Risk Level
• Loan Amount Risk
• Anomaly Detection
• Reasoning

Current implementation: agents/financial_risk_agent.py

Important rule:

Deterministic financial calculations and thresholds must be
implemented in Python/rules, not invented by the LLM.

Claude should be used for reasoning, interpretation and explanation.

────────

Agent 3 — Loan Decision Agent

MCP: DecisionSynthesis

Must return:

• Classification: APPROVE / REJECT / REVIEW
• Risk Score
• Confidence Level
• Key Decision Factors
• Explanation

Current implementation: agents/decision_agent.py

Current MCP: mcp_server/decision_synthesis_server.py

────────

Agent 4 — Compliance & Action Orchestrator Agent

Case-study MCP name: NotificationSystem

Must return:

• Action Taken
• Notification Sent
• Case ID
• Timestamp
• Summary

Current implementation: agents/compliance_agent.py

Current MCP implementation: mcp_server/compliance_server.py

The current Compliance MCP combines: - KYC checking - blacklist
checking - document completeness - notification/action creation

Do NOT split this into another MCP merely for naming unless the
requirement/evaluator specifically requires it.

────────

5. Current Implemented Architecture — DO NOT REDESIGN

The current repository already implements:

```text
Streamlit UI
      |
      v
FastAPI POST /loan/apply
      |
      v
LangGraph Orchestrator
      |
      +--> Applicant Agent --> ApplicantDB MCP
      |
      +--> Financial Risk Agent --> RiskRulesDB MCP
      |
      +--> Compliance Agent --> Compliance MCP
      |
      +--> Decision Agent --> DecisionSynthesis MCP
      |
      v
APPROVE / REJECT / REVIEW
      |
      v
Streamlit result display
```

Current LangGraph sequence

```text
START
  |
Applicant Agent
  |
Financial Risk Agent
  |
Compliance Agent
  |
Decision Agent
  |
END
```

The case study’s agent responsibility list mentions Decision before
Compliance, but the implemented workflow uses Compliance before
Decision. The implemented order is intentional because the final
decision consumes the compliance result.

Do not reorder the graph unless there is a clear requirement or
explicit user request.

────────

6. Current Repository Structure

```text
Agentic-AI-Loan-Approval-System/
|
├── agents/
│   ├── applicant_agent.py
│   ├── financial_risk_agent.py
│   ├── compliance_agent.py
│   └── decision_agent.py
|
├── api/
│   └── main.py
|
├── mcp_server/
│   ├── applicant_server.py
│   ├── risk_rules_server.py
│   ├── compliance_server.py
│   └── decision_synthesis_server.py
|
├── models/
│   └── schemas.py
|
├── orchestration/
│   ├── graph.py
│   └── state.py
|
├── tests/
│   ├── test_compliance.py
│   ├── test_decision_synthesis.py
│   ├── test_risk_agent.py
│   ├── test_risk_rules.py
│   ├── test_graph.py
│   └── test_run_workflow.py
|
├── ui/
│   └── streamlit_app.py
|
├── README.md
├── casestudydocument.txt
└── requirements.txt
```

__init__.py files, where present, are Python package markers. Empty
__init__.py files are normally valid and should not be deleted just
because they are empty.

────────

7. Data Models

Primary models are in:

models/schemas.py

Important models:

LoanApplication

```text
applicant_id
name
age
annual_income
employment_type
credit_score
loan_amount
loan_term
existing_liabilities
location
application_timestamp
```

ApplicantProfileResult

```text
income_stability_score
employment_risk
credit_history_summary
application_complete
risk_score
rationale
```

FinancialRiskResult

```text
debt_to_income_ratio
credit_score_risk
loan_amount_risk
anomaly_detected
risk_score
risk_level
reasoning
```

ComplianceActionResult

```text
compliance_status
action_taken
notification_sent
case_id
timestamp
summary
```

LoanDecisionResult

```text
classification
risk_score
confidence_level
key_decision_factors
explanation
```

────────

8. MCP Responsibilities

ApplicantDB MCP

File: mcp_server/applicant_server.py

Purpose: - retrieve applicant profile by applicant ID

Tool: get_applicant(applicant_id)

Used by: Applicant Agent

────────

RiskRulesDB MCP

File: mcp_server/risk_rules_server.py

Purpose: - provide financial risk rules/thresholds

Tool: get_risk_rules()

Current sample rules include: - maximum DTI: 50% - minimum credit score:
650 - high loan amount threshold: ₹50,000 - high risk score threshold:
70

────────

Compliance MCP

File: mcp_server/compliance_server.py

Purpose: - KYC - blacklist - document checks - notification/action

Tools include: - check_compliance(applicant_id) -
send_notification(...)

────────

DecisionSynthesis MCP

File: mcp_server/decision_synthesis_server.py

Purpose: - apply final decision rules

Tool: make_loan_decision(risk_score, compliance_ok, credit_score)

Current decision rules:

```text
If compliance fails OR credit score < 650
    -> REVIEW

Else if risk score >= 70
    -> REJECT

Else
    -> APPROVE
```

Preserve these rules unless the user explicitly asks to change them.

────────

9. LangGraph State

File: orchestration/state.py

The shared state is conceptually:

```text
application
applicant_profile
financial_risk
compliance_result
decision
```

File: orchestration/graph.py

This is the workflow coordinator.

Do not add unnecessary agents, nodes, state fields or branches unless
they are required.

────────

10. FastAPI

File: api/main.py

Primary endpoint:

```text
POST /loan/apply
```

Purpose: 1. receive loan application 2. validate request through
Pydantic models 3. invoke LangGraph 4. return the complete workflow
result

Health endpoint is also available.

Do not bypass LangGraph from the API.

────────

11. Streamlit

File: ui/streamlit_app.py

Purpose: - collect applicant/application data - call FastAPI - display
final decision - display risk analysis - display compliance/action
information - display explanation and decision factors - optionally show
raw API response for debugging

The UI is currently form-based/interactive rather than a full
conversational chatbot.

Do not redesign it into a chatbot unless explicitly requested.

────────

12. Technology Stack

Required/implemented technologies:

• Python 3.x
• Anthropic Claude
• Claude Sonnet 4.6 as the current documented model
• LangGraph
• LangChain where already used
• FastMCP/MCP
• FastAPI
• Streamlit
• Pydantic
• Pytest
• Prompt engineering
• Claude Code

Do not introduce a new framework/library when the existing stack can
solve the task.

────────

13. Explainability Requirements

Every final decision should be understandable.

The final result should preserve:

• classification
• risk score
• confidence
• key decision factors
• explanation
• relevant compliance result
• relevant risk reasoning

Do not replace explainable fields with a single opaque LLM response.

────────

14. Important Design Principles

Principle 1 — Preserve the existing architecture

Do not rebuild the project.

Before changing code: 1. Inspect the relevant existing file. 2.
Understand how it connects to the workflow. 3. Make the smallest
required change. 4. Run the relevant test. 5. Report the result.

Principle 2 — One task at a time

Do not implement multiple unrelated features in one change.

Preferred workflow:

```text
Requirement
  ↓
Inspect
  ↓
Small change
  ↓
Test
  ↓
Verify
  ↓
Next task
```

Principle 3 — Minimal token usage

Claude Code should: - inspect only relevant files first - avoid reading
the entire repository repeatedly - avoid rewriting working files - avoid
generating unnecessary documentation/code - avoid repeating the complete
architecture in every response - make focused patches - give concise
progress summaries

Principle 4 — Do not invent project requirements

Use this file + existing repository + explicit user request as the
source of truth.

If something is not specified: - inspect the existing implementation
first - preserve current behavior - do not invent a new architecture

Principle 5 — No unnecessary dependency changes

Do not add packages unless required.

If a package is already available, reuse it.

Principle 6 — Keep deterministic logic deterministic

Financial formulas, thresholds and classification rules should be
deterministic and testable in Python/MCP rules.

Use Claude for: - reasoning - interpretation - summarization -
natural-language explanation

Do not let the LLM invent numerical calculations that should be
deterministic.

────────

15. Current Known Limitations — Preserve Unless Fix Is Requested

The current repository documents these limitations:

1. ApplicantDB has sample/static applicants.
2. Compliance data is sample/hardcoded.
3. Risk rules are basic thresholds.
4. All agents use the same Claude model.
5. No persistent loan database/audit history.
6. No API authentication/authorization.
7. MCP calls are sequential/synchronous.

These are known limitations, not bugs to automatically fix.

If improving them, do so as separate small tasks.

────────

16. Evaluation Requirements

The evaluator may check:

Architecture

• Can the developer explain Agentic AI architecture?
• Can they explain why there are multiple agents?
• Can they explain LangGraph?
• Can they explain MCP?

Agent responsibilities

Be able to explain:

```text
Applicant Agent
    = applicant/profile analysis

Financial Risk Agent
    = financial risk analysis

Compliance Agent
    = KYC/blacklist/documents/actions

Decision Agent
    = final loan decision
```

MCP

Be able to explain:

```text
Agent
  |
  v
MCP tool
  |
  v
Data/operation
  |
  v
Result returned to agent
```

Live modification

Code should remain understandable and modular so a small requirement can
be changed during evaluation.

Explainability

Final decision must show why it was made.

────────

17. Development History / How This Project Was Built

The project was intentionally developed incrementally with Claude Code
rather than asking Claude Code to generate the whole application at
once.

Development approach:

```text
1. Understand case study
2. Set up Python/environment
3. Test Claude API
4. Build Applicant Profile Agent
5. Build Financial Risk Agent
6. Build Loan Decision Agent
7. Build Compliance/Action Agent
8. Define Pydantic data models
9. Add LangGraph orchestration/state
10. Add MCP servers/tools
11. Connect agents to MCP
12. Add FastAPI
13. Add Streamlit
14. Add tests
15. Verify end-to-end workflow
16. Prepare README/evaluation explanation
```

For future work, continue with the same incremental approach.

────────

18. Preferred Claude Code Working Protocol

When the user gives a new task, Claude Code should follow this protocol:

Step A — Understand

Read: - this Project_requirement.md - only the relevant existing
file(s)

Step B — Inspect

Explain briefly: - what currently exists - where the requested change
belongs - what files will be changed

Step C — Implement

Make the smallest possible change.

Step D — Test

Run the most relevant existing test(s).

Step E — Verify

Confirm: - what changed - whether tests passed - whether existing
behavior was preserved

Step F — Stop

Do not continue implementing unrelated improvements.

────────

19. Prompt Template for Small Claude Code Tasks

Use this pattern:

```text
Read Project_requirement.md first.

Task:
<ONE SMALL TASK>

Constraints:
- Preserve the existing architecture.
- Do not rewrite unrelated code.
- Inspect the relevant file before changing it.
- Make the smallest change required.
- Reuse existing models/functions where possible.
- Run the relevant test after the change.
- Keep the response concise.
- Do not implement the next task automatically.
```

Example:

```text
Read Project_requirement.md first.

Task:
Fix the ApplicantDB so a new applicant can be added without changing Python source code.

Constraints:
- Do not redesign the agent workflow.
- Inspect the current ApplicantDB implementation first.
- Make only the changes needed for this task.
- Keep existing AP001/AP002 behavior working.
- Run the relevant tests.
- Do not modify unrelated files.
```

────────

20. What Claude Code Must NOT Do

Unless explicitly requested:

• Do not rebuild the project.
• Do not replace LangGraph.
• Do not replace MCP.
• Do not replace FastAPI.
• Do not replace Streamlit.
• Do not create a completely new architecture.
• Do not create extra agents.
• Do not create extra MCP servers.
• Do not rewrite all files.
• Do not change decision rules silently.
• Do not move functionality between agents without a requirement.
• Do not add dependencies unnecessarily.
• Do not optimize unrelated code.
• Do not modify tests just to make a failing implementation pass.
• Do not remove empty __init__.py files simply because they are
empty.
• Do not assume a documented limitation is a bug unless the user asks
to fix it.

────────

21. Quick Reference — Whole Project in One View

```text
USER
 |
 v
STREAMLIT
 |
 v
FASTAPI /loan/apply
 |
 v
LANGGRAPH
 |
 +--> APPLICANT AGENT
 |       |
 |       +--> ApplicantDB MCP
 |
 +--> FINANCIAL RISK AGENT
 |       |
 |       +--> RiskRulesDB MCP
 |
 +--> COMPLIANCE AGENT
 |       |
 |       +--> Compliance MCP
 |             +--> KYC
 |             +--> Blacklist
 |             +--> Documents
 |             +--> Notification/Action
 |
 +--> DECISION AGENT
         |
         +--> DecisionSynthesis MCP
                |
                v
       APPROVE / REJECT / REVIEW
                |
                v
          EXPLANATION
                |
                v
            STREAMLIT
```

22. Final Source-of-Truth Rule

For every future change, prioritize information in this order:

1. Explicit user request
2. This Project_requirement.md
3. Current working repository/code
4. Original case-study requirements
5. General best practices

The existing project is the baseline. Improve it incrementally; do not
recreate it.

Goal: Keep the implementation aligned with the case study while
keeping the code understandable enough for the user to explain and
modify during live evaluation.