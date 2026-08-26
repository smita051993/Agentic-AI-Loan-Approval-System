from mcp.server import MCPServer
mcp = MCPServer("ComplianceDB")

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

if __name__ == "__main__":
   mcp.run()