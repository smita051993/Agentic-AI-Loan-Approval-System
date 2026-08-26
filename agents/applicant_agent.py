import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel


# -----------------------------
# Loan Application Model
# -----------------------------

class LoanApplication(BaseModel):

    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    loan_tenure: int
    existing_liabilities: float
    location: str


class ApplicantProfileResult(BaseModel):
   income_stability_score: int
   employment_risk: str
   credit_history_summary: str
   application_complete: bool
   risk_score: int
   rationale: str


# -----------------------------

# Claude Configuration

# -----------------------------

load_dotenv(override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:

    raise ValueError("ANTHROPIC_API_KEY not found")

client = Anthropic(api_key=api_key)


# -----------------------------

# Sample Application

# -----------------------------

application = LoanApplication(

    applicant_id="APP1001",

    age=32,

    income=80000,

    employment_type="Salaried",

    credit_score=780,

    loan_amount=2000000,

    loan_tenure=10,

    existing_liabilities=10000,

    location="Bangalore"

)


# -----------------------------
# Applicant Profile Agent
# -----------------------------

def analyze_applicant(application):

    prompt = f"""

You are the Applicant Profile Agent

in an intelligent loan approval system.

Analyze this loan application:

{json.dumps(application, indent=2)}

Evaluate:

1. Income stability

2. Employment risk

3. Credit history

4. Application completeness

5. Overall applicant profile risk

Return ONLY valid JSON.

The JSON MUST contain exactly these fields:

{{

    "income_stability_score": 0,

    "employment_risk": "LOW",

    "credit_history_summary": "",

    "application_complete": true,

    "risk_score": 0,

    "rationale": ""

}}

Rules:

- income_stability_score must be between 0 and 100.

- risk_score must be between 0 and 100.

- employment_risk must be LOW, MEDIUM, or HIGH.

- application_complete must be true or false.

- Do not include markdown.

- Do not include ```json.

- Do not make the final loan decision.

- Only analyze the applicant profile.

"""
 
    response = client.messages.create(

        model="claude-sonnet-4-6",

        max_tokens=500,

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    result= response.content[0].text
    return ApplicantProfileResult.model_validate_json(result)


# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":

    result = analyze_applicant(application)
    print("\n===== APPLICANT PROFILE AGENT =====")
    print(result)
    print("\n===== AS DICTIONARY =====")
    print(result.model_dump())

 