import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
async def test_decision(risk_score, compliance_ok, credit_score, expected):
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/decision_synthesis_server.py"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "make_loan_decision",
                arguments={
                    "risk_score": risk_score,
                    "compliance_ok": compliance_ok,
                    "credit_score": credit_score,
                },
            )
            # Convert MCP response to text for validation
            result_text = str(result)
            print(
                f"\nRisk={risk_score}, "
                f"Compliance={compliance_ok}, "
                f"Credit={credit_score}"
            )
            print("Result:", result)
            # Verify expected decision
            assert expected in result_text, (
                f"Expected {expected}, but got: {result_text}"
            )
async def main():
    print("=== Decision Synthesis MCP Tests ===")
    # 1. Low-risk applicant → APPROVE
    await test_decision(
        risk_score=40,
        compliance_ok=True,
        credit_score=750,
        expected="APPROVE",
    )
    # 2. Compliance failure → REVIEW
    await test_decision(
        risk_score=40,
        compliance_ok=False,
        credit_score=750,
        expected="REVIEW",
    )
    # 3. Low credit score → REVIEW
    await test_decision(
        risk_score=40,
        compliance_ok=True,
        credit_score=600,
        expected="REVIEW",
    )
    # 4. High risk → REJECT
    await test_decision(
        risk_score=80,
        compliance_ok=True,
        credit_score=750,
        expected="REJECT",
    )
    # 5. Boundary: risk score 70 → REJECT
    await test_decision(
        risk_score=70,
        compliance_ok=True,
        credit_score=750,
        expected="REJECT",
    )
    print("\nAll decision synthesis tests passed!")
if __name__ == "__main__":
    asyncio.run(main())