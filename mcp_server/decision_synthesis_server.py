from mcp.server import MCPServer

mcp = MCPServer("DecisionSynthesis")


@mcp.tool()
def make_loan_decision(
    risk_score: int,
    credit_score: int
) -> dict:
    """Synthesize the final loan decision."""

    if risk_score >= 70:
        return {
            "classification": "REJECT",
            "risk_score": risk_score,
            "confidence_level": 0.95,
            "key_decision_factors": [
                "High financial risk"
            ],
            "explanation": "Application has a high financial risk score."
        }

    if credit_score < 650:
        return {
            "classification": "REVIEW",
            "risk_score": risk_score,
            "confidence_level": 0.80,
            "key_decision_factors": [
                "Low credit score"
            ],
            "explanation": "Credit score is below the required threshold."
        }

    return {
        "classification": "APPROVE",
        "risk_score": risk_score,
        "confidence_level": 0.90,
        "key_decision_factors": [
            "Acceptable risk score",
            "Valid credit score"
        ],
        "explanation": "Application meets the available decision criteria."
    }


if __name__ == "__main__":
    mcp.run()