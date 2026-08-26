from mcp.server import MCPServer
mcp = MCPServer("CreditDB")

CREDIT_DATA = {
   "AP001": {
       "credit_score": 720,
       "existing_loans": 1,
       "outstanding_amount": 150000,
       "payment_history": "GOOD"
   },
   "AP002": {
       "credit_score": 650,
       "existing_loans": 3,
       "outstanding_amount": 450000,
       "payment_history": "AVERAGE"
   }
}

@mcp.tool()
def get_credit_information(applicant_id: str) -> dict:
   """Retrieve credit information for an applicant."""
   credit = CREDIT_DATA.get(applicant_id)
   if not credit:
       return {
           "error": "Credit information not found"
       }
   return credit

if __name__ == "__main__":
   mcp.run()