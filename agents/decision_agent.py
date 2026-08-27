import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from models.schemas import LoanDecisionResult


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

{json.dumps(
    applicant_profile.model_dump(),
    indent=2
)}

Financial Risk:

{json.dumps(
    financial_risk.model_dump(),
    indent=2
)}


Based ONLY on the information provided above:

Classify the application as exactly ONE of:

APPROVE
REJECT
REVIEW


Return:

1. classification
2. risk_score from 0 to 100
3. confidence_level from 0 to 1
4. key_decision_factors
5. explanation


Do not invent information.

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.

Return exactly this structure:

{{
    "classification": "APPROVE",
    "risk_score": 25,
    "confidence_level": 0.90,
    "key_decision_factors": [
        "Stable employment",
        "Good credit score",
        "Low debt-to-income ratio"
    ],
    "explanation": "The application presents low financial risk based on the available applicant and financial information."
}}
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
