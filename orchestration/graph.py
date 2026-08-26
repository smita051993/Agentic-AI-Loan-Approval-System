from langgraph.graph import StateGraph, START, END
from orchestration.state import LoanState
from agents.applicant_agent import analyze_applicant
from agents.financial_risk_agent import analyze_financial_risk
from agents.decision_agent import make_loan_decision
from agents.compliance_agent import compliance_agent
# ============================================================
# Applicant Agent Node
# ============================================================
def applicant_node(state: LoanState):
   application = state["application"]
   result = analyze_applicant(application)
   return {
       "applicant_profile": result
   }

# ============================================================
# Financial Risk Agent Node
# ============================================================
def financial_risk_node(state: LoanState):
   application = state["application"]
   applicant_profile = state["applicant_profile"]
   result = analyze_financial_risk(
       application,
       applicant_profile
   )
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
   return {
       "decision": result
   }

# ============================================================
# Build LangGraph
# ============================================================
builder = StateGraph(LoanState)

# Add nodes
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
# Define workflow
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
# Compile graph
# ============================================================
loan_graph = builder.compile()