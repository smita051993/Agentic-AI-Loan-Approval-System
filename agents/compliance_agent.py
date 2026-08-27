import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def compliance_agent(state):
    """
    Compliance Agent

    Calls the Compliance MCP Server to check
    KYC, blacklist and document compliance.
    """

    application = state["application"]

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

        # Check compliance
    is_compliant = (
        compliance_check["kyc_verified"]
        and not compliance_check["blacklisted"]
        and compliance_check["documents_complete"]
    )
    if is_compliant:
        action_taken = "NO_ACTION"
        notification_sent = False
        case_id = None
    else:
        action_taken = "MANUAL_REVIEW"
        notification_sent = True
        case_id = f"CASE-{applicant_id}"

    compliance_result = {
        "compliance_check": compliance_check,
        "compliance_status": "PASS" if is_compliant else "FAIL",
        "action_taken": action_taken,
        "notification_sent": notification_sent,
        "case_id": case_id
    }

    print("\n[Compliance Agent] Completed")
    print("Compliance Result:", compliance_result)

    return {
        "compliance_result": compliance_result
    }