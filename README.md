Agentic-AI-Loan-Approval-System/
│
├── agents/
│   ├── applicant_agent.py
│   ├── financial_risk_agent.py
│   ├── decision_agent.py
│   └── compliance_agent.py
│
├── orchestration/
│   ├── state.py
│   └── graph.py
│
├── mcp_servers/
│   ├── applicant_server.py
│   ├── risk_server.py
│   └── decision_server.py
│
├── api/
│   └── main.py
│
├── ui/
│   └── app.py
│
├── models/
│   └── schemas.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md




if st.button("Submit Application"):

    application = {
        "applicant_id": applicant_id,
        "name": name,
        "age": age,
        "income": income,
        "credit_score": credit_score,
        "employment_type": employment_type,
        "loan_amount": loan_amount,
        "debt_obligations": debt_obligations
    }

    st.subheader("Application Submitted")
    st.json(application)

    # Send application to FastAPI
    try:
        response = requests.post(
            "http://127.0.0.1:8000/loan/apply",
            json=application
        )

        if response.status_code == 200:
            result = response.json()

            st.success("Loan application processed successfully!")

            st.subheader("AI Loan Decision")
            st.json(result)

        else:
            st.error(
                f"FastAPI returned error {response.status_code}"
            )
            st.write(response.text)

    except Exception as e:
        st.error(f"Could not connect to FastAPI: {e}")
