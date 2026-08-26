from pydantic import BaseModel

class LoanApplication(BaseModel):
   name: str
   age: int
   annual_income: float
   employment_type: str
   loan_amount: float
   loan_term: int
   credit_score: int

class ApplicantProfileResult(BaseModel):
   income_stability_score: float
   employment_risk: str
   credit_history_summary: str
   risk_score: float
   rationale: str

class FinancialRiskResult(BaseModel):
   risk_score: float
   debt_to_income_ratio: float
   risk_level: str
   rationale: str

class LoanDecisionResult(BaseModel):
   classification: str
   risk_score: float
   confidence_level: float
   explanation: str