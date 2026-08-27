import asyncio
import json
import uuid
from datetime import datetime

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def compliance_agent(state):
    """
    Compliance Agent

    Calls the Compliance MCP Server to check
    KYC, blacklist and document compliance.
    """

    application = state["application"]
    decision = state["decision"]

    # Get applicant ID
    if isinstance(application, dict):
        applicant_id = application["applicant_id"]
    else:
        applicant_id = application.applicant_id

    # Start Compliance MCP Server
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/compliance_server.py"],
    )

    # Connect to MCP server
    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize MCP session
            await session.initialize()

            # Call MCP compliance tool
            result = await session.call_tool(
                "check_compliance",
                arguments={
                    "applicant_id": applicant_id
                },
            )

    # Extract MCP response
    mcp_text = result.content[0].text
    compliance_check = json.loads(mcp_text)

    # Handle applicant not found
    if "error" in compliance_check:
        return {
            "compliance_result": compliance_check
        }

    # Generate case information
    case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.now().isoformat()

    # Check compliance
    is_compliant = (
        compliance_check["kyc_verified"]
        and not compliance_check["blacklisted"]
        and compliance_check["documents_complete"]
    )

    # Decide final action
    if is_compliant and decision.classification == "APPROVE":

        action_taken = "Loan application approved"
        notification_sent = True

    elif not is_compliant:

        action_taken = "Loan application rejected due to compliance failure"
        notification_sent = True

    elif decision.classification == "REJECT":

        action_taken = "Loan application rejected"
        notification_sent = True

    else:

        action_taken = "Loan application sent for manual review"
        notification_sent = True

    # Create summary
    summary = (
        f"Loan application {decision.classification}. "
        f"Compliance status: {'PASS' if is_compliant else 'FAIL'}. "
        f"Action taken: {action_taken}. "
        f"Case ID: {case_id}."
    )

    compliance_result = {
        "compliance_check": compliance_check,
        "compliance_status": "PASS" if is_compliant else "FAIL",
        "action_taken": action_taken,
        "notification_sent": notification_sent,
        "case_id": case_id,
        "timestamp": timestamp,
        "summary": summary,
    }

    return {
        "compliance_result": compliance_result
    }