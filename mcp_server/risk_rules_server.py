from mcp.server.mcpserver import MCPServer
mcp = MCPServer("RiskRulesDB")


RISK_RULES = {
    "max_debt_to_income_ratio": 0.50,
    "minimum_credit_score": 650,
    "high_loan_amount": 50000,
    "high_risk_score": 70
}


@mcp.tool()
def get_risk_rules() -> dict:
    """
    Retrieve financial risk rules for loan evaluation.
    """
    return RISK_RULES


if __name__ == "__main__":
    mcp.run()