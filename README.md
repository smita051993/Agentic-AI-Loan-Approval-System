# Agentic AI Loan Approval System

An intelligent multi-agent loan approval system powered by Claude AI, LangGraph, and MCP servers. This system automates loan assessment through coordinated AI agents that evaluate applicant profiles, financial risk, compliance requirements, and make data-driven lending decisions.

## Project Overview

The Agentic AI Loan Approval System is designed to streamline the loan approval process by leveraging multiple specialized AI agents working together in a coordinated workflow. Each agent focuses on a specific aspect of loan evaluation:

- **Applicant Profile Analysis**: Assesses income stability, employment risk, credit history, and application completeness
- **Financial Risk Assessment**: Evaluates debt-to-income ratios, credit scores, loan amounts, and detects anomalies
- **Compliance Verification**: Checks KYC (Know Your Customer), blacklist status, and document completeness
- **Decision Synthesis**: Synthesizes all evaluations into a final loan decision (APPROVE, REJECT, or REVIEW)

The system provides both a REST API and an interactive Streamlit web interface for loan applications and result visualization.

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI                             │
│                  (Interactive Interface)                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI Server                                │
│              (REST API Endpoints)                               │
│            POST /loan/apply                                     │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  LangGraph Workflow                             │
│         (Orchestrates Agent Execution)                          │
└──┬──────────┬──────────┬──────────┬────────────┬────────────────┘
   │          │          │          │            │
   ▼          ▼          ▼          ▼            ▼
┌──────┐ ┌────────┐ ┌────────┐ ┌──────────┐ ┌────────┐
│ App  │ │Finan.  │ │Compli. │ │Decision  │ │Applicant
│Agent │ │Risk    │ │Agent   │ │Agent     │ │Profile
│      │ │Agent   │ │        │ │          │ │MCP
└──────┘ └────────┘ └────────┘ └──────────┘ └────────┘
   │          │          │          │            │
   └──────────┴──────────┴──────────┴────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│              4 MCP Servers (Tool Providers)                     │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Claude AI**: Anthropic's Claude Sonnet for natural language reasoning
- **LangGraph**: Workflow orchestration and state management
- **FastAPI**: High-performance REST API framework
- **Streamlit**: Interactive web UI for loan applications
- **MCP (Model Context Protocol)**: Tool integration and external data access
- **Pydantic**: Data validation and schema management
- **Python 3.13+**: Core runtime

---

## MCP Servers (4)

MCP (Model Context Protocol) servers provide tools that agents use to access data and perform operations.

### 1. **ApplicantDB Server** (`mcp_server/applicant_server.py`)
- **Purpose**: Manages applicant database and profile information
- **Tools**:
  - `get_applicant(applicant_id)` - Retrieves applicant information by ID
- **Used By**: Applicant Agent
- **Sample Data**:
  - AP001: John Doe (Full-time, Credit: 720)
  - AP002: Jane Smith (Contract, Credit: 650)

### 2. **RiskRulesDB Server** (`mcp_server/risk_rules_server.py`)
- **Purpose**: Provides financial risk evaluation rules and thresholds
- **Tools**:
  - `get_risk_rules()` - Returns risk evaluation parameters
- **Used By**: Financial Risk Agent
- **Rules Provided**:
  - Max debt-to-income ratio: 0.50 (50%)
  - Minimum credit score: 650
  - High loan amount threshold: ₹50,000
  - High risk score threshold: 70

### 3. **Compliance Server** (`mcp_server/compliance_server.py`)
- **Purpose**: Handles KYC, blacklist, and document compliance checks
- **Tools**:
  - `check_compliance(applicant_id)` - Verifies KYC, blacklist, and document status
  - `send_notification(...)` - Creates compliance actions and notifications
- **Used By**: Compliance Agent
- **Checks**:
  - KYC verification status
  - Blacklist status
  - Document completeness

### 4. **DecisionSynthesis Server** (`mcp_server/decision_synthesis_server.py`)
- **Purpose**: Synthesizes loan decisions based on risk scores and compliance
- **Tools**:
  - `make_loan_decision(risk_score, compliance_ok, credit_score)` - Generates final decision
- **Used By**: Decision Agent
- **Decision Logic**:
  - REVIEW: If compliance fails or credit score < 650
  - REJECT: If risk score ≥ 70
  - APPROVE: If all criteria are met

---

## Agents (4)

Agents are AI-powered decision-makers that use Claude AI to analyze information and make recommendations.

### 1. **Applicant Agent** (`agents/applicant_agent.py`)
- **Role**: Evaluates applicant profile and personal financial situation
- **Process**:
  1. Calls ApplicantDB Server to fetch applicant information
  2. Uses Claude AI to analyze:
     - Income stability score
     - Employment risk level
     - Credit history summary
     - Application completeness
     - Risk score (0-100)
- **Output**: `ApplicantProfileResult`
  - Income stability score
  - Employment risk (LOW/MEDIUM/HIGH)
  - Credit history summary
  - Application complete flag
  - Risk score

### 2. **Financial Risk Agent** (`agents/financial_risk_agent.py`)
- **Role**: Conducts detailed financial risk analysis
- **Process**:
  1. Fetches risk evaluation rules from RiskRulesDB
  2. Analyzes applicant and application data using Claude AI
  3. Calculates:
     - Debt-to-income ratio
     - Credit score risk assessment
     - Loan amount risk classification
     - Anomaly detection
     - Overall risk score (0-100)
- **Output**: `FinancialRiskResult`
  - Debt-to-income ratio
  - Credit score risk (LOW/MEDIUM/HIGH)
  - Loan amount risk (LOW/MEDIUM/HIGH)
  - Anomaly detected flag
  - Risk score and level

### 3. **Compliance Agent** (`agents/compliance_agent.py`)
- **Role**: Verifies regulatory and compliance requirements
- **Process**:
  1. Calls Compliance Server to check KYC status
  2. Verifies blacklist status and document completeness
  3. Generates compliance status (PASS/FAIL)
  4. Creates notifications and actions for manual review if needed
- **Output**: `ComplianceActionResult`
  - Compliance status (PASS/FAIL)
  - Action taken (NO_ACTION/MANUAL_REVIEW)
  - Notification sent status
  - Case ID (if manual review needed)

### 4. **Decision Agent** (`agents/decision_agent.py`)
- **Role**: Synthesizes all evaluations into final lending decision
- **Process**:
  1. Collects results from all previous agents
  2. Calls DecisionSynthesis Server with:
     - Aggregated risk score
     - Compliance status
     - Credit score
  3. Applies decision rules to determine final outcome
- **Output**: `LoanDecisionResult`
  - Classification (APPROVE/REJECT/REVIEW)
  - Risk score
  - Confidence level
  - Key decision factors
  - Detailed explanation

---

## LangGraph Workflow

The orchestration uses LangGraph to coordinate agent execution in a deterministic workflow.

### Workflow Sequence

```
START
  │
  ▼
┌─────────────────────────────────┐
│  1. APPLICANT AGENT NODE       │
│  Analyzes applicant profile    │
│  → ApplicantProfileResult      │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  2. FINANCIAL RISK AGENT NODE   │
│  Evaluates financial risk       │
│  → FinancialRiskResult          │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  3. COMPLIANCE AGENT NODE       │
│  Checks compliance requirements │
│  → ComplianceActionResult       │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  4. DECISION AGENT NODE         │
│  Synthesizes final decision     │
│  → LoanDecisionResult           │
└──────────────┬──────────────────┘
               │
               ▼
              END
```

### LangGraph State

The `LoanState` TypedDict maintains workflow state:

```python
class LoanState(TypedDict):
    application: LoanApplication
    applicant_profile: ApplicantProfileResult
    financial_risk: FinancialRiskResult
    decision: LoanDecisionResult
    compliance_result: dict
```

### Orchestration File

- **Location**: `orchestration/graph.py`
- **Compiled Graph**: `loan_graph` - Async-ready LangGraph for workflow execution

---

## FastAPI Backend

### Server

- **Location**: `api/main.py`
- **Framework**: FastAPI
- **Port**: 8000 (default)

### Endpoints

#### Health Check
```
GET /
Response: { "message": "Agentic AI Loan Approval System is running" }
```

#### Loan Application
```
POST /loan/apply
Content-Type: application/json

Request Body:
{
  "applicant_id": "AP001",
  "name": "John Doe",
  "age": 35,
  "annual_income": 85000,
  "employment_type": "FULL_TIME",
  "credit_score": 720,
  "loan_amount": 30000,
  "loan_term": 5,
  "existing_liabilities": 5000,
  "location": "Bangalore",
  "application_timestamp": "2024-08-28T10:00:00"
}

Response:
{
  "status": "success",
  "result": {
    "application": {...},
    "applicant_profile": {...},
    "financial_risk": {...},
    "compliance_result": {...},
    "decision": {...}
  }
}
```

---

## Streamlit UI

### User Interface

- **Location**: `ui/streamlit_app.py`
- **Port**: 8501 (default)

### Features

1. **Applicant Details Form**
   - Applicant ID, Name, Age
   - Annual Income, Loan Amount, Credit Score
   - Employment Type, Loan Tenure, Debt Obligations
   - Location

2. **AI Loan Decision Display**
   - Large decision badge (APPROVE/REJECT/REVIEW)
   - Risk score and confidence level
   - Risk level classification

3. **Applicant Information Summary**
   - Personal and financial data
   - Formatted currency values

4. **Financial Risk Assessment**
   - Risk score, Credit score risk
   - Debt-to-income ratio
   - Anomaly detection status

5. **Key Decision Factors**
   - Bullet-list summary of decision rationale

6. **AI Risk Reasoning**
   - Expandable section with detailed reasoning

7. **Compliance Results**
   - Action taken (NO_ACTION/MANUAL_REVIEW)
   - Notification status
   - Case ID (if applicable)

8. **Complete API Response**
   - Expandable raw JSON for debugging

---

## Data Models

### Schemas Location
- **File**: `models/schemas.py`

### Core Models

#### LoanApplication
```python
applicant_id: str
name: str
age: int
annual_income: float
employment_type: str
credit_score: int
loan_amount: float
loan_term: int
existing_liabilities: float
location: str
application_timestamp: str
```

#### ApplicantProfileResult
```python
income_stability_score: float
employment_risk: str          # LOW, MEDIUM, HIGH
credit_history_summary: str
application_complete: bool
risk_score: float
rationale: str
```

#### FinancialRiskResult
```python
debt_to_income_ratio: float
credit_score_risk: str        # LOW, MEDIUM, HIGH
loan_amount_risk: str         # LOW, MEDIUM, HIGH
anomaly_detected: bool
risk_score: int
risk_level: str               # LOW, MEDIUM, HIGH
reasoning: str
```

#### LoanDecisionResult
```python
classification: str           # APPROVE, REJECT, REVIEW
risk_score: int
confidence_level: float
key_decision_factors: list[str]
explanation: str
```

#### ComplianceActionResult
```python
compliance_status: str        # PASS, FAIL
action_taken: str            # NO_ACTION, MANUAL_REVIEW
notification_sent: bool
case_id: str | None
timestamp: str
summary: str
```

---

## How to Run the Project

### Prerequisites

- Python 3.13+
- `pip` or `uv` package manager
- ANTHROPIC_API_KEY environment variable set

### Installation

1. **Clone or navigate to project directory**
   ```bash
   cd Agentic-AI-Loan-Approval-System
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file in project root
   echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
   ```

### Running the System

#### Option 1: FastAPI + Streamlit (Recommended)

**Terminal 1: Start FastAPI Server**
```bash
python -m uvicorn api.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2: Start Streamlit UI**
```bash
streamlit run ui/streamlit_app.py --server.port 8501
```

Expected output:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

Then open your browser to `http://localhost:8501` and submit a loan application.

#### Option 2: API Testing via cURL

```bash
# Start FastAPI server first
python -m uvicorn api.main:app --reload

# In another terminal, test the API
curl -X POST http://localhost:8000/loan/apply \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "AP001",
    "name": "John Doe",
    "age": 35,
    "annual_income": 85000,
    "employment_type": "FULL_TIME",
    "credit_score": 720,
    "loan_amount": 30000,
    "loan_term": 5,
    "existing_liabilities": 5000,
    "location": "Bangalore",
    "application_timestamp": "2024-08-28T10:00:00"
  }'
```

---

## How to Run the Tests

### Test Files

The project includes 6 comprehensive test files:

1. **test_compliance.py** - Tests compliance agent
2. **test_decision_synthesis.py** - Tests decision synthesis MCP server
3. **test_risk_agent.py** - Tests financial risk agent
4. **test_risk_rules.py** - Tests risk rules MCP server
5. **test_graph.py** - Tests LangGraph workflow
6. **test_run_workflow.py** - End-to-end workflow test

### Running Tests

**Run all tests:**
```bash
pytest tests/
```

**Run specific test:**
```bash
pytest tests/test_graph.py -v
pytest tests/test_compliance.py -v
pytest tests/test_run_workflow.py -v
```

**Run with verbose output:**
```bash
pytest tests/ -v -s
```

### Individual Test Scripts

Tests can also be run as standalone scripts:

```bash
# Test compliance workflow
python tests/test_compliance.py

# Test decision synthesis
python tests/test_decision_synthesis.py

# Test financial risk agent
python tests/test_risk_agent.py

# Test risk rules MCP
python tests/test_risk_rules.py

# End-to-end workflow test
python tests/test_run_workflow.py

# Full graph workflow test (high-risk applicant scenario)
python tests/test_graph.py
```

---

## Test Scenarios and Results

### Scenario 1: Compliant, Low-Risk Applicant (AP001)
- **Profile**: John Doe, Full-time, Credit Score: 720
- **Income**: ₹85,000, Loan Request: ₹30,000
- **Expected Decision**: APPROVE
- **Reasoning**: Meets all criteria - good credit, low risk, compliant

### Scenario 2: Partial Compliance, Medium-Risk Applicant (AP002)
- **Profile**: Jane Smith, Contract, Credit Score: 650
- **Income**: ₹45,000, Loan Request: ₹30,000
- **Documents**: Incomplete
- **Expected Decision**: REVIEW
- **Reasoning**: Missing compliance documents - requires manual review

### Scenario 3: High-Risk Applicant
- **Profile**: High-risk test case
- **Income**: ₹30,000, Loan Request: ₹100,000
- **Credit Score**: 550 (below minimum)
- **Expected Decision**: REJECT or REVIEW
- **Reasoning**: High loan-to-income ratio, low credit score

### Test Execution Output Example

```
[Applicant Node] Completed
Applicant Profile: {
  "income_stability_score": 8.5,
  "employment_risk": "LOW",
  "credit_history_summary": "Good payment history",
  "application_complete": true,
  "risk_score": 25
}

[Financial Risk Node] Completed
Financial Risk: {
  "debt_to_income_ratio": 0.35,
  "credit_score_risk": "LOW",
  "loan_amount_risk": "LOW",
  "anomaly_detected": false,
  "risk_score": 30,
  "risk_level": "LOW"
}

[Compliance Node] Completed
Compliance Result: {
  "compliance_status": "PASS",
  "action_taken": "NO_ACTION",
  "notification_sent": false,
  "case_id": null
}

[Decision Node] Completed
Decision: {
  "classification": "APPROVE",
  "risk_score": 30,
  "confidence_level": 0.90,
  "key_decision_factors": ["Acceptable risk score", "Valid credit score"],
  "explanation": "Application meets available decision criteria."
}
```

---

## Known Limitations

1. **Static Applicant Database**: Only AP001 and AP002 are pre-configured in ApplicantDB. New applicants require code updates.

2. **Sample Compliance Rules**: Hardcoded compliance status in database. Real implementation needs external compliance service integration.

3. **Limited Risk Rules**: Risk evaluation rules are basic thresholds. Production systems need more sophisticated risk models.

4. **Single Claude Model**: All agents use Claude Sonnet 4.6. Specialized models could be used for specific agents.

5. **No Persistent State**: Loan applications are not stored in a database. No audit trail or historical tracking.

6. **No Authentication**: API has no authentication/authorization. Production needs security layers.

7. **Synchronous MCP Calls**: Each agent makes synchronous MCP calls, which could be parallelized for performance.

8. **Limited Error Handling**: Minimal validation of edge cases and error scenarios.

---

## Future Improvements

1. **Persistent Database**: Integrate PostgreSQL/MongoDB for loan application history and audit trails.

2. **Real Compliance Integration**: Connect to actual KYC, AML, and document verification services.

3. **Advanced Risk Models**: Implement machine learning models for more accurate risk scoring.

4. **API Authentication**: Add JWT/OAuth2 for secure API access.

5. **Webhook Notifications**: Real-time notifications for approval/rejection decisions.

6. **Admin Dashboard**: Management interface for reviewing pending applications and compliance cases.

7. **Performance Optimization**: Parallel agent execution and MCP call optimization.

8. **Monitoring & Logging**: Structured logging and performance metrics collection.

9. **Multi-Tenancy**: Support multiple financial institutions with separate rules and data.

10. **A/B Testing**: Framework for testing different decision strategies and risk models.

---

## Project Structure

```
Agentic-AI-Loan-Approval-System/
├── api/
│   ├── __init__.py
│   └── main.py                    # FastAPI application
├── agents/
│   ├── applicant_agent.py         # Applicant profile analysis
│   ├── financial_risk_agent.py    # Financial risk assessment
│   ├── decision_agent.py          # Decision synthesis
│   └── compliance_agent.py        # Compliance verification
├── mcp_server/
│   ├── __init__.py
│   ├── applicant_server.py        # ApplicantDB MCP server
│   ├── risk_rules_server.py       # RiskRulesDB MCP server
│   ├── compliance_server.py       # Compliance MCP server
│   └── decision_synthesis_server.py # Decision synthesis MCP server
├── models/
│   ├── __init__.py
│   └── schemas.py                 # Pydantic data models
├── orchestration/
│   ├── __init__.py
│   ├── graph.py                   # LangGraph workflow definition
│   └── state.py                   # LangGraph state schema
├── ui/
│   └── streamlit_app.py           # Streamlit web interface
├── tests/
│   ├── test_compliance.py
│   ├── test_decision_synthesis.py
│   ├── test_risk_agent.py
│   ├── test_risk_rules.py
│   ├── test_graph.py
│   └── test_run_workflow.py
├── requirements.txt               # Project dependencies
├── .env                          # Environment variables (not in repo)
└── README.md                     # This file
```

---

## Dependencies

See `requirements.txt` for complete list:

- **anthropic**: Claude AI API client
- **langgraph**: Workflow orchestration
- **mcp[cli]**: Model Context Protocol support
- **fastapi**: REST API framework
- **uvicorn**: ASGI server
- **streamlit**: Web UI framework
- **pydantic**: Data validation
- **python-dotenv**: Environment variable management
- **requests**: HTTP client library
- **uv**: Python package management

---

## Support & Troubleshooting

### Common Issues

**1. ANTHROPIC_API_KEY not found**
```bash
# Solution: Set environment variable
export ANTHROPIC_API_KEY="your-api-key"
# Or create .env file with: ANTHROPIC_API_KEY=your-api-key
```

**2. FastAPI port already in use**
```bash
# Use different port
python -m uvicorn api.main:app --reload --port 8001
```

**3. Streamlit connection refused**
```bash
# Ensure FastAPI is running on port 8000
# Check firewall settings if needed
```

**4. MCP server initialization error**
```bash
# Ensure Python path is correct
# Check mcp_server files are executable
chmod +x mcp_server/*.py
```

**5. Claude API rate limit exceeded**
```bash
# Wait a few seconds before retrying
# Optimize prompt lengths to reduce token usage
```

---

## License

This project is part of the Capstone Project for Agentic AI development.

---

## Contributing

This is an educational capstone project. For improvements or bug fixes, please:
1. Test changes thoroughly
2. Update relevant test files
3. Document changes in this README
4. Ensure backward compatibility

---

**Last Updated**: August 28, 2024
