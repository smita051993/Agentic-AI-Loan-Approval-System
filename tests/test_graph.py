import asyncio
from orchestration.graph import loan_graph
async def main():
    # -----------------------------
    # Sample Loan Application
    # -----------------------------
    application = {
        "applicant_id": "AP002",
        "name": "High Risk Applicant",
        "age": 35,
        "annual_income": 30000,
        "credit_score": 550,
        "loan_amount": 100000,
        "loan_term": 10,
        "employment_type": "Contract",
        "existing_liabilities": 0,
        "location": "Bangalore",
    }
    # -----------------------------
    # Run LangGraph Workflow
    # -----------------------------
    result = await loan_graph.ainvoke({
        "application": application
    })
    # -----------------------------
    # Validate Workflow Results
    # -----------------------------
    assert result.get("applicant_profile") is not None, (
        "Applicant Profile Agent did not return a result"
    )
    assert result.get("financial_risk") is not None, (
        "Financial Risk Agent did not return a result"
    )
    assert result.get("compliance_result") is not None, (
        "Compliance Agent did not return a result"
    )
    assert result.get("decision") is not None, (
        "Decision Agent did not return a result"
    )
    # -----------------------------
    # Display Results
    # -----------------------------
    print("\n==============================")
    print("FINAL LOAN APPROVAL RESULT")
    print("==============================")
    print("\nApplicant Profile:")
    print(result["applicant_profile"])
    print("\nFinancial Risk:")
    print(result["financial_risk"])
    print("\nCompliance:")
    print(result["compliance_result"])
    print("\nLoan Decision:")
    print(result["decision"])
    print("\n==============================")
    print("LangGraph workflow test passed!")
    print("==============================")
if __name__ == "__main__":
    asyncio.run(main())