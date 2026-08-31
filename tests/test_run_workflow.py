from orchestration.graph import loan_graph
from orchestration.state import LoanState


def main():
    # -----------------------------
    # Sample Loan Application
    # -----------------------------
    application = {
        "applicant_id": "AP001",
        "name": "John Doe",
        "age": 32,
        "annual_income": 80000,
        "employment_type": "Salaried",
        "credit_score": 780,
        "loan_amount": 2000000,
        "loan_term": 10,
        "existing_liabilities": 10000,
        "location": "Bangalore",
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

    # -----------------------------
    # Compliance & Action
    # -----------------------------
    print("\n==============================")
    print("     COMPLIANCE & ACTION")
    print("==============================")

    compliance = result.get("compliance_result", {})

    print("Action Taken      :", compliance.get("action_taken"))
    print("Notification Sent :", compliance.get("notification_sent"))
    print("Case ID            :", compliance.get("case_id"))
    print("Timestamp          :", compliance.get("timestamp"))
    print("Summary            :", compliance.get("summary"))

    print("\n==============================")


if __name__ == "__main__":
    main()