from mcp.server.mcpserver import MCPServer
from datetime import datetime
mcp = MCPServer("NotificationSystem")

COMPLIANCE_RULES = {
   "AP001": {
       "kyc_verified": True,
       "blacklisted": False,
       "documents_complete": True
   },
   "AP002": {
       "kyc_verified": True,
       "blacklisted": False,
       "documents_complete": False
   }
}

@mcp.tool()
def check_compliance(applicant_id: str) -> dict:
   """Check compliance information for an applicant."""
   applicant = COMPLIANCE_RULES.get(applicant_id)
   if not applicant:
       return {
           "error": "Applicant compliance information not found"
       }
   return applicant

@mcp.tool()
def send_notification(
   applicant_id: str,
   compliance_status: str,
   action_taken: str,
   summary: str
) -> dict:
   """Create notification and compliance action details."""
   notification_sent = action_taken != "NO_ACTION"
   case_id = (
       f"CASE-{applicant_id}"
       if action_taken == "MANUAL_REVIEW"
       else None
   )
   return {
       "compliance_status": compliance_status,
       "action_taken": action_taken,
       "notification_sent": notification_sent,
       "case_id": case_id,
       "timestamp": datetime.now().isoformat(),
       "summary": summary
   }

if __name__ == "__main__":
   mcp.run()