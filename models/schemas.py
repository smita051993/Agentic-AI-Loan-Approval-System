from pydantic import BaseModel

class LoanApplication(BaseModel):
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

class ApplicantProfileResult(BaseModel):
   income_stability_score: float
   employment_risk: str
   credit_history_summary: str
   application_complete: bool
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