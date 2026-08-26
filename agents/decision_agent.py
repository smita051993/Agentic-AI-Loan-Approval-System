import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel

# ---------------------------------------
# Loan Decision Result
# ---------------------------------------
class LoanDecisionResult(BaseModel):
   classification: str
   risk_score: int
   confidence_level: float
   key_decision_factors: list[str]
   explanation: str

# ---------------------------------------
# Claude Configuration
# ---------------------------------------
load_dotenv(override=True)
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
   raise ValueError("ANTHROPIC_API_KEY not found")
client = Anthropic(api_key=api_key)

# ---------------------------------------
# Decision Agent
# ---------------------------------------
def make_loan_decision(
   application,
   applicant_profile,
   financial_risk
):
   prompt = f"""
You are the Loan Decision Agent
in an intelligent loan approval system.
Your responsibility is to synthesize the
outputs from the Applicant Profile Agent
and Financial Risk Agent.
Original Loan Application:
{json.dumps(application, indent=2)}
Applicant Profile:
{json.dumps(applicant_profile.model_dump(), indent=2)}
Financial Risk:
{json.dumps(financial_risk.model_dump(), indent=2)}
Based ONLY on the information provided above,
classify the application as exactly one of:
APPROVE
REJECT
REVIEW
Return:
- classification
- risk_score from 0 to 100
- confidence_level from 0 to 1
- key_decision_factors
- explanation
Do not invent information.
Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.
"""
   response = client.messages.create(
       model="claude-sonnet-4-6",
       max_tokens=800,
       messages=[
           {
               "role": "user",
               "content": prompt
           }
       ]
   )
   result = response.content[0].text.strip()
   validated_result = LoanDecisionResult.model_validate_json(result)
   return validated_result


# # TESTING- TEMPORARY ADD

# if __name__ == "__main__":
#    from applicant_agent import (
#        application,
#        analyze_applicant
#    )
#    from financial_risk_agent import (
#        analyze_financial_risk
#    )
#    # Agent 1
#    applicant_profile = analyze_applicant(application)
   

#    # Agent 2
#    financial_risk = analyze_financial_risk(
#        application,
#        applicant_profile
#    )


#    # Agent 3
#    decision = make_loan_decision(
#        application,
#        applicant_profile,
#        financial_risk
#    )
#    print("\n========== APPLICANT PROFILE ==========")
# print(f"Income Stability : {applicant_profile.income_stability_score}")
# print(f"Employment Risk  : {applicant_profile.employment_risk}")
# print(f"Credit Score     : {application.credit_score}")
# print(f"Application      : {'COMPLETE' if applicant_profile.application_complete else 'INCOMPLETE'}")

# print("\n========== FINANCIAL RISK ==========")
# print(f"Debt-to-Income   : {financial_risk.debt_to_income_ratio:.1%}")
# print(f"Credit Risk      : {financial_risk.credit_score_risk}")
# print(f"Loan Amount Risk : {financial_risk.loan_amount_risk}")
# print(f"Anomaly          : {financial_risk.anomaly_detected}")

# print("\n========== LOAN DECISION ==========")
# print(f"Decision         : {decision.classification}")
# print(f"Risk Score       : {decision.risk_score}")
# print(f"Confidence       : {decision.confidence_level:.0%}")
# print(f"Reason           : {decision.explanation}")