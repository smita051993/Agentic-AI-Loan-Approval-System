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
    debt_to_income_ratio: float
    credit_score_risk: str
    loan_amount_risk: str
    anomaly_detected: bool
    risk_score: int
    risk_level: str
    reasoning: str

class LoanDecisionResult(BaseModel):
   classification: str
   risk_score: int
   confidence_level: float
   key_decision_factors: list[str]
   explanation: str