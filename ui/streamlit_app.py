import streamlit as st
import requests

st.set_page_config( page_title="Agentic AI Loan Approval System", 
                   page_icon="", layout="centered" )

st.title("Agentic AI Loan Approval System") 
st.write("Submit a loan application for AI-powered assessment.")

st.subheader("Applicant Details")

applicant_id = st.text_input("Applicant ID", "APP001") 
name = st.text_input("Name", "John Doe") 
age = st.number_input("Age", min_value=18, max_value=100, value=35)

income = st.number_input( "Annual Income", min_value=0.0, value=85000.0 )

credit_score = st.number_input( "Credit Score", min_value=300, max_value=900, value=720 )

employment_type = st.selectbox( "Employment Type", ["PERMANENT", "CONTRACT", "SELF_EMPLOYED", "UNEMPLOYED"] )

loan_amount = st.number_input( "Loan Amount", min_value=0.0, value=30000.0 )

debt_obligations = st.number_input( "Debt Obligations", min_value=0.0, value=5000.0 )

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