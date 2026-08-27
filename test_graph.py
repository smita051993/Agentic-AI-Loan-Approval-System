import asyncio
from orchestration.graph import loan_graph

# application = {
#    "name": "Low Risk Applicant",
#    "age": 35,
#    "annual_income": 100000,
#    "credit_score": 720,
#    "loan_amount": 20000,
#    "employment_status": "employed"
# }
# application = {
#    "name": "Medium Risk Applicant",
#    "age": 35,
#    "annual_income": 45000,
#    "credit_score": 680,
#    "loan_amount": 30000,
#    "employment_status": "employed"
# }
application = {
   "applicant_id": "APP001",
   "name": "High Risk Applicant",
   "age": 35,
   "annual_income": 30000,
   "credit_score": 550,
   "loan_amount": 100000,
   "employment_status": "contract",
   "debt_obligations": 0
}
# application = {
#    "name": "Approved Applicant",
#    "age": 35,
#    "annual_income": 85000,
#    "credit_score": 720,
#    "loan_amount": 15000,
#    "employment_status": "employed"
# }
# application = {
#    "applicant_id": "APP001",
#    "name": "John Doe",
#    "age": 35,
#    "income": 85000,
#    "credit_score": 720,
#    "employment_type": "PERMANENT",
#    "loan_amount": 30000,
#    "debt_obligations": 5000
# }



async def main():
   result = await loan_graph.ainvoke({
       "application": application
   })
   print("\nApplicant Profile:")
   print(result["applicant_profile"])
   print("\nFinancial Risk:")
   print(result["financial_risk"])
   print("\nDecision:")
   print(result["decision"])
   print("\nCompliance:")
   print(result["compliance_result"])

asyncio.run(main())