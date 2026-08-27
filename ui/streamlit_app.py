import streamlit as st
import requests

API_URL = "http://localhost:8000/loan/apply"
 

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

    st.subheader("Application Details")
    st.json(application)

    # Send application to FastAPI
    try:
        with st.spinner("⏳ Processing your loan application... Please wait"):

            response = requests.post(
            API_URL,
            json=application
            )

        if response.status_code == 200:
            result = response.json()

            st.success("Loan application processed successfully!")

            # Get LangGraph result
            data = result.get("result", {})

            # Get individual sections
            application_data = data.get("application", {})
            applicant_profile = data.get("applicant_profile", {})
            financial_risk = data.get("financial_risk", {})
            decision = data.get("decision", {})
            compliance = data.get("compliance_result", {})

            # -----------------------------
            # AI LOAN DECISION
            # -----------------------------

            st.header(" AI Loan Decision")

            classification = decision.get("classification", "N/A")
            risk_score = decision.get("risk_score", "N/A")
            confidence = decision.get("confidence_level", 0)

            # Decision
            if classification == "APPROVE":
                st.success(f" {classification}")
            elif classification == "REJECT":
                st.error(f" {classification}")
            else:
                st.warning(f" {classification}")

            # Metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Risk Score", risk_score)

            with col2:
                st.metric("Confidence", f"{confidence * 100:.0f}%")

            with col3:
                st.metric(
                    "Employment",
                    application_data.get("employment_type", "N/A")
                )

            # -----------------------------
            # APPLICANT INFORMATION
            # -----------------------------

            st.subheader(" Applicant Information")

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"**Applicant ID:** "
                    f"{application_data.get('applicant_id', 'N/A')}"
                )

                st.write(
                    f"**Name:** "
                    f"{application_data.get('name', 'N/A')}"
                )

                st.write(
                    f"**Age:** "
                    f"{application_data.get('age', 'N/A')}"
                )

            with col2:
                st.write(
                    f"**Income:** "
                    f"₹{application_data.get('income', 0):,.0f}"
                )

                st.write(
                    f"**Loan Amount:** "
                    f"₹{application_data.get('loan_amount', 0):,.0f}"
                )

                st.write(
                    f"**Debt Obligations:** "
                    f"₹{application_data.get('debt_obligations', 0):,.0f}"
                )

            # -----------------------------
            # FINANCIAL RISK
            # -----------------------------

            st.subheader("📊 Financial Risk Assessment")

            risk_level = financial_risk.get(
                "risk_level",
                financial_risk.get("risk", "N/A")
            )

            st.write(f"**Risk Level:** {risk_level}")

            # -----------------------------
            # DECISION FACTORS
            # -----------------------------

            st.subheader("🔍 Key Decision Factors")

            factors = decision.get("key_decision_factors", [])

            if factors:
                for factor in factors:
                    st.write(f"• {factor}")
            else:
                st.write("No decision factors available.")

            # -----------------------------
            # COMPLIANCE
            # -----------------------------

            st.subheader(" Compliance")

            action = compliance.get("action_taken", "N/A")
            notification = compliance.get("notification_sent", False)
            case_id = compliance.get("case_id", "N/A")

            st.write(f"**Action:** {action}")
            st.write(
                f"**Notification Sent:** "
                f"{' Yes' if notification else '❌ No'}"
            )
            st.write(f"**Case ID:** {case_id}")

            # -----------------------------
            # RAW RESPONSE
            # -----------------------------

            # with st.expander(" View Complete API Response"):
            #     st.json(result)

        else:
            st.error(
                f"FastAPI returned error {response.status_code}"
            )
            st.write(response.text)

    except Exception as e:
        st.error(f"Could not connect to FastAPI: {e}")