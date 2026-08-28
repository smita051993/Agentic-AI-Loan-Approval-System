import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from models.schemas import LoanDecisionResult


async def make_loan_decision(
    application,
    applicant_profile,
    financial_risk,
    compliance_result
):
    """
    Decision Agent

    Calls Decision Synthesis MCP Server to generate
    the final loan decision.
    """

    # -------------------------------------------------
    # Convert application to dictionary
    # -------------------------------------------------

    if hasattr(application, "model_dump"):
        application_data = application.model_dump()
    else:
        application_data = application

    # -------------------------------------------------
    # Convert applicant profile to dictionary
    # -------------------------------------------------

    if hasattr(applicant_profile, "model_dump"):
        applicant_profile_data = applicant_profile.model_dump()
    else:
        applicant_profile_data = applicant_profile

    # -------------------------------------------------
    # Convert financial risk to dictionary
    # -------------------------------------------------

    if hasattr(financial_risk, "model_dump"):
        financial_risk_data = financial_risk.model_dump()
    else:
        financial_risk_data = financial_risk

    # -------------------------------------------------
    # Compliance result is normally a dictionary
    # -------------------------------------------------

    if hasattr(compliance_result, "model_dump"):
        compliance_data = compliance_result.model_dump()
    else:
        compliance_data = compliance_result

    # -------------------------------------------------
    # Extract required values
    # -------------------------------------------------

    credit_score = int(application_data["credit_score"])

    risk_score = int(financial_risk_data["risk_score"])

    compliance_ok = (
            compliance_data.get("compliance_status") == "PASS"
    )

    # -------------------------------------------------
    # Start Decision Synthesis MCP Server
    # -------------------------------------------------

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/decision_synthesis_server.py"],
    )

    # -------------------------------------------------
    # Connect to MCP server
    # -------------------------------------------------

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            # -------------------------------------------------
            # Call Decision Synthesis MCP Tool
            # -------------------------------------------------

            result = await session.call_tool(
                "make_loan_decision",
                arguments={
                    "risk_score": risk_score,
                    "compliance_ok": compliance_ok,
                    "credit_score": credit_score,
                },
            )

    # -------------------------------------------------
    # Extract MCP response
    # -------------------------------------------------

    mcp_text = result.content[0].text

    decision_data = json.loads(mcp_text)

    # -------------------------------------------------
    # Validate using Pydantic schema
    # -------------------------------------------------

    validated_result = LoanDecisionResult.model_validate(
        decision_data
    )

    return validated_result