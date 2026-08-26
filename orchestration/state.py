from typing import TypedDict
from agents.applicant_agent import (
   LoanApplication,
   ApplicantProfileResult
)
from agents.financial_risk_agent import (
   FinancialRiskResult
)
from agents.decision_agent import (
   LoanDecisionResult
)

class LoanState(TypedDict, total=False):
   # Original loan application
   application: LoanApplication
   # Output from Applicant Profile Agent
   applicant_profile: ApplicantProfileResult
   # Output from Financial Risk Agent
   financial_risk: FinancialRiskResult
   # Output from Decision Agent
   decision: LoanDecisionResult

   compliance_result : dict