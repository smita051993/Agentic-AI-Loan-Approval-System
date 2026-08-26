from orchestration.graph import loan_graph
from orchestration.state import LoanState

def main():
   # -----------------------------
   # Sample Loan Application
   # -----------------------------
   application = {
       "applicant_id": "APP1001",
       "age": 32,
       "income": 80000,
       "employment_type": "Salaried",
       "credit_score": 780,
       "loan_amount": 2000000,
       "loan_tenure": 10,
       "existing_liabilities": 10000,
       "location": "Bangalore"
   }
   # -----------------------------
   # Initial LangGraph State
   # -----------------------------
   initial_state: LoanState = {
       "application": application
   }
   # -----------------------------
   # Run Workflow
   # -----------------------------
   result = loan_graph.invoke(initial_state)
   # -----------------------------
   # Display Results
   # -----------------------------
   print("\n==============================")
   print("       LOAN DECISION")
   print("==============================")
   print("\nApplicant Profile:")
   print(result.get("applicant_profile"))
   print("\nFinancial Risk:")
   print(result.get("financial_risk"))
   print("\nFinal Decision:")
   print(result.get("decision"))

   print("\n==============================")

   print("COMPLIANCE & ACTION")

   print("==============================")
   print("Action Taken      :", result["compliance_result"]["action_taken"])
   print("Notification Sent :", result["compliance_result"]["notification_sent"])
   print("Case ID            :", result["compliance_result"]["case_id"])
   print("Timestamp          :", result["compliance_result"]["timestamp"])
   print("Summary            :", result["compliance_result"]["summary"])
 
   
if __name__ == "__main__":
   main()