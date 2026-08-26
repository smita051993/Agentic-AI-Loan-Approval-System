from typing import TypedDict
from models.schemas import (
   LoanApplication,
   ApplicantProfileResult,
   FinancialRiskResult,
   LoanDecisionResult
)

class LoanState(TypedDict, total=False):
   application: LoanApplication
   applicant_profile: ApplicantProfileResult
   financial_risk: FinancialRiskResult
   decision: LoanDecisionResult
   compliance_result: dict