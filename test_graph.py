import asyncio
from orchestration.graph import loan_graph

application = {
   "name": "Jane Smith",
   "age": 29,
   "annual_income": 45000,
   "credit_score": 720,
   "loan_amount": 20000,
   "employment_status": "employed"
}



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