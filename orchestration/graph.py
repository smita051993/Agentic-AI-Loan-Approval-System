from langgraph.graph import StateGraph, START, END

from orchestration.state import LoanState

from agents.applicant_agent import analyze_applicant
from agents.financial_risk_agent import analyze_financial_risk
from agents.decision_agent import make_loan_decision
from agents.compliance_agent import compliance_agent


# ============================================================
# Applicant Agent Node
# ============================================================
async def applicant_node(state: LoanState):

    result = await analyze_applicant(state)

    print("\n[Applicant Node] Completed")
    print("Applicant Profile:", result)

    return {
        "applicant_profile": result
    }


# ============================================================
# Financial Risk Agent Node
# ============================================================
async def financial_risk_node(state: LoanState):

    application = state["application"]
    applicant_profile = state["applicant_profile"]

    result = await analyze_financial_risk(
        application,
        applicant_profile
    )

    print("\n[Financial Risk Node] Completed")
    print("Financial Risk:", result)

    return {
        "financial_risk": result
    }


# ============================================================
# Decision Agent Node
# ============================================================
def decision_node(state: LoanState):

    application = state["application"]
    applicant_profile = state["applicant_profile"]
    financial_risk = state["financial_risk"]

    result = make_loan_decision(
        application,
        applicant_profile,
        financial_risk
    )

    print("\n[Decision Node] Completed")
    print("Decision:", result)

    return {
        "decision": result
    }


# ============================================================
# Build Graph
# ============================================================
builder = StateGraph(LoanState)


builder.add_node(
    "applicant",
    applicant_node
)

builder.add_node(
    "financial_risk",
    financial_risk_node
)

builder.add_node(
    "decision",
    decision_node
)

builder.add_node(
    "compliance",
    compliance_agent
)


# ============================================================
# Workflow
# ============================================================
builder.add_edge(
    START,
    "applicant"
)

builder.add_edge(
    "applicant",
    "financial_risk"
)

builder.add_edge(
    "financial_risk",
    "decision"
)

builder.add_edge(
    "decision",
    "compliance"
)

builder.add_edge(
    "compliance",
    END
)


# ============================================================
# Compile
# ============================================================
loan_graph = builder.compile()