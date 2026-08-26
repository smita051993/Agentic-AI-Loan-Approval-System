import os

import json

from dotenv import load_dotenv

from anthropic import Anthropic

from pydantic import BaseModel


# -----------------------------

# Output Model

# -----------------------------

class FinancialRiskResult(BaseModel):

    debt_to_income_ratio: float

    credit_score_risk: str

    loan_amount_risk: str

    anomaly_detected: bool

    risk_score: int

    reasoning: str


# -----------------------------

# Claude Configuration

# -----------------------------

load_dotenv(override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:

    raise ValueError("ANTHROPIC_API_KEY not found")

client = Anthropic(api_key=api_key)


# -----------------------------

# Financial Risk Agent

# -----------------------------

def analyze_financial_risk(application, applicant_profile):

    prompt = f"""

You are the Financial Risk Analysis Agent

in an intelligent loan approval system.

Analyze the financial risk of the applicant.

Loan Application:

{json.dumps(application, indent=2)}

Applicant Profile Analysis:

{json.dumps(applicant_profile.model_dump(), indent=2)}

Evaluate:

1. Debt-to-income ratio

2. Credit score risk

3. Loan amount risk

4. Anomaly detection

5. Overall risk score from 0 to 100

6. Reasoning

IMPORTANT:

Return ONLY valid JSON.

Do not use markdown.

Do not use ```json.

Do not add explanations before or after the JSON.

Return exactly:

{{

    "debt_to_income_ratio": 0.0,

    "credit_score_risk": "LOW",

    "loan_amount_risk": "MEDIUM",

    "anomaly_detected": false,

    "risk_score": 25,

    "reasoning": "..."

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

    # Claude response

    result = response.content[0].text.strip()

    # Remove markdown fences if Claude adds them

    if result.startswith("```"):

        result = result.replace("```json", "")

        result = result.replace("```", "")

        result = result.strip()

    # Convert JSON string → dictionary

    data = json.loads(result)

    # Validate dictionary using Pydantic

    validated_result = FinancialRiskResult.model_validate(data)

    return validated_result
 