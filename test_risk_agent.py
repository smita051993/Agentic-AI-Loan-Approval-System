import asyncio

from agents.financial_risk_agent import analyze_financial_risk


application = {
    "applicant_id": "AP002",
    "name": "High Risk Applicant",
    "age": 35,
    "annual_income": 30000,
    "credit_score": 550,
    "loan_amount": 100000,
    "employment_status": "contract",
    "debt_obligations": 0
}


applicant_profile = {
    "applicant_id": "AP002",
    "name": "High Risk Applicant"
}


async def main():

    result =await analyze_financial_risk(
        application,
        applicant_profile
    )

    print("\nFinancial Risk Result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())