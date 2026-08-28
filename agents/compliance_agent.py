import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from models.schemas import ComplianceActionResult


async def compliance_agent(state):
    """
    Compliance Agent

    Calls the Compliance MCP Server to:
    1. Check KYC, blacklist and document compliance
    2. Create action/notification details
    """

    application = state["application"]

    # Get applicant ID
    if isinstance(application, dict):
        applicant_id = application["applicant_id"]
    else:
        applicant_id = application.applicant_id

    # --------------------------------------------------
    # Start Compliance MCP Server
    # --------------------------------------------------
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/compliance_server.py"],
    )

    # --------------------------------------------------
    # Connect to MCP Server
    # --------------------------------------------------
    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize MCP session
            await session.initialize()

            # --------------------------------------------------
            # 1. Check Compliance
            # --------------------------------------------------
            result = await session.call_tool(
                "check_compliance",
                arguments={
                    "applicant_id": applicant_id
                },
            )

            # Extract MCP response
            mcp_text = result.content[0].text
            compliance_check = json.loads(mcp_text)

            # Applicant compliance data not found
            if "error" in compliance_check:
                raise ValueError(compliance_check["error"])

            # --------------------------------------------------
            # 2. Evaluate Compliance
            # --------------------------------------------------
            is_compliant = (
                compliance_check["kyc_verified"]
                and not compliance_check["blacklisted"]
                and compliance_check["documents_complete"]
            )

            if is_compliant:
                compliance_status = "PASS"
                action_taken = "NO_ACTION"
                summary = "Application passed compliance checks."
            else:
                compliance_status = "FAIL"
                action_taken = "MANUAL_REVIEW"
                summary = (
                    "Application requires manual review "
                    "due to compliance checks."
                )

            # --------------------------------------------------
            # 3. Call Notification/Action MCP Tool
            # --------------------------------------------------
            notification_result = await session.call_tool(
                "send_notification",
                arguments={
                    "applicant_id": applicant_id,
                    "compliance_status": compliance_status,
                    "action_taken": action_taken,
                    "summary": summary
                },
            )

            # Extract notification/action response
            notification_text = notification_result.content[0].text
            notification_data = json.loads(notification_text)

    # --------------------------------------------------
    # 4. Create final ComplianceActionResult
    # --------------------------------------------------
    compliance_result = ComplianceActionResult(
            compliance_status=compliance_status,
            action_taken=notification_data["action_taken"],
            notification_sent=notification_data["notification_sent"],
            case_id=notification_data["case_id"],
            timestamp=notification_data["timestamp"],
            summary=notification_data["summary"]
    )
    # --------------------------------------------------
    # 5. Logging
    # --------------------------------------------------
    print("\n[Compliance Agent] Completed")
    print("Compliance Result:", compliance_result)

    # --------------------------------------------------
    # 6. Return to LangGraph
    # --------------------------------------------------
    return {
        "compliance_result": compliance_result
    }