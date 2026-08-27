from mcp.server import MCPServer

mcp = MCPServer("DecisionSynthesis")


@mcp.tool()
def make_loan_decision(
    risk_score: int,
    compliance_ok: bool,
    credit_score: int
) -> dict:
    """Synthesize the final loan decision."""

    if not compliance_ok:
        return {
            "classification": "Review",
            "risk_score": risk_score,
            "confidence_level": "High",
            "key_decision_factors": [
                "Compliance requirements not satisfied"
            ],
            "explanation": "Application requires manual review due to compliance issues."
        }

    if risk_score >= 70:
        return {
            "classification": "Reject",
            "risk_score": risk_score,
            "confidence_level": "High",
            "key_decision_factors": [
                "High financial risk"
            ],
            "explanation": "Application has a high financial risk score."
        }

    if credit_score < 650:
        return {
            "classification": "Review",
            "risk_score": risk_score,
            "confidence_level": "Medium",
            "key_decision_factors": [
                "Low credit score"
            ],
            "explanation": "Credit score is below the required threshold."
        }

    return {
        "classification": "Approve",
        "risk_score": risk_score,
        "confidence_level": "High",
        "key_decision_factors": [
            "Acceptable risk score",
            "Valid compliance status",
            "Acceptable credit score"
        ],
        "explanation": "Application meets the available decision criteria."
    }


if __name__ == "__main__":
    mcp.run()