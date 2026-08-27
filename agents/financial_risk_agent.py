import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from models.schemas import FinancialRiskResult


# -----------------------------
# Claude Configuration
# -----------------------------

load_dotenv(override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found")

client = Anthropic(api_key=api_key)


# -----------------------------
# Get Risk Rules from MCP
# -----------------------------

async def get_risk_rules_from_mcp():

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/risk_rules_server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "get_risk_rules",
                arguments={}
            )

    # MCP response
    mcp_text = result.content[0].text

    risk_rules = json.loads(mcp_text)

    return risk_rules

def to_dict(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return obj
# -----------------------------
# Financial Risk Agent
# -----------------------------

async def analyze_financial_risk(application, applicant_profile):

    # Get rules from MCP
    risk_rules = await get_risk_rules_from_mcp()

    print("\nRisk Rules received from MCP:")
    print(risk_rules)

    prompt = f"""

You are the Financial Risk Analysis Agent
in an intelligent loan approval system.

Analyze the financial risk of the applicant.

Loan Application:

{json.dumps(to_dict(application), indent=2)}

Applicant Profile Analysis:

{json.dumps(to_dict(applicant_profile), indent=2)}

Financial Risk Rules from Risk Rules MCP:

{json.dumps(risk_rules, indent=2)}

Use these rules when evaluating the applicant.

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
    "risk_level": "LOW",
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

    result = response.content[0].text.strip()

    # Remove markdown fences if necessary
    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    data = json.loads(result)

    validated_result = FinancialRiskResult.model_validate(data)

    return validated_result