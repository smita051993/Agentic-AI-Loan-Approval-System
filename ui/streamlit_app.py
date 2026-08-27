import streamlit as st
import requests

API_URL = "http://localhost:8000/loan/apply"


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Agentic AI Loan Approval System",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    .decision-box {
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        margin: 20px 0;
    }

    .approve {
        background-color: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #81c784;
    }

    .reject {
        background-color: #ffebee;
        color: #c62828;
        border: 1px solid #ef9a9a;
    }

    .review {
        background-color: #fff8e1;
        color: #f57f17;
        border: 1px solid #ffcc80;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">Agentic AI Loan Approval System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Submit a loan application for AI-powered risk assessment and decisioning.'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# APPLICANT DETAILS
# ==================================================

st.markdown(
    '<div class="section-title">Applicant Details</div>',
    unsafe_allow_html=True
)


# Use TWO equal columns
# This keeps all fields compact and aligned.

col1, col2 = st.columns(2)


# --------------------------------------------------
# LEFT COLUMN
# --------------------------------------------------

with col1:

    applicant_id = st.text_input(
        "Applicant ID",
        "AP001"
    )

    name = st.text_input(
        "Name",
        "John Doe"
    )

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=35
    )

    income = st.number_input(
        "Annual Income",
        min_value=0.0,
        value=85000.0
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0,
        value=30000.0
    )


# --------------------------------------------------
# RIGHT COLUMN
# --------------------------------------------------

with col2:

    credit_score = st.number_input(
        "Credit Score",
        min_value=300,
        max_value=900,
        value=720
    )

    employment_type = st.selectbox(
        "Employment Type",
        [
            "PERMANENT",
            "CONTRACT",
            "SELF_EMPLOYED",
            "UNEMPLOYED"
        ]
    )

    loan_tenure = st.number_input(
        "Loan Tenure (Years)",
        min_value=1,
        max_value=30,
        value=5
    )

    debt_obligations = st.number_input(
        "Debt Obligations",
        min_value=0.0,
        value=5000.0
    )

    location = st.text_input(
        "Location",
        "Bangalore"
    )


# ==================================================
# SUBMIT APPLICATION
# ==================================================

if st.button(
    "Submit Application",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------
    # APPLICATION JSON
    # --------------------------------------------------

    application = {
        "applicant_id": applicant_id,
        "name": name,
        "age": age,
        "income": income,
        "credit_score": credit_score,
        "employment_type": employment_type,
        "loan_amount": loan_amount,
        "loan_tenure": loan_tenure,
        "debt_obligations": debt_obligations,
        "location": location
    }


    # --------------------------------------------------
    # PROCESS APPLICATION
    # --------------------------------------------------

    try:

        with st.spinner(
            "Please wait!!! AI agents are processing your loan application..."
        ):

            response = requests.post(
                API_URL,
                json=application,
                timeout=120
            )


        # ==================================================
        # SUCCESS RESPONSE
        # ==================================================

        if response.status_code == 200:

            result = response.json()

            st.success(
                "Loan application processed successfully!"
            )


            # --------------------------------------------------
            # GET LANGGRAPH RESULT
            # --------------------------------------------------

            data = result.get("result", {})

            application_data = data.get(
                "application",
                {}
            )

            applicant_profile = data.get(
                "applicant_profile",
                {}
            )

            financial_risk = data.get(
                "financial_risk",
                {}
            )

            decision = data.get(
                "decision",
                {}
            )

            compliance = data.get(
                "compliance_result",
                {}
            )


            # ==================================================
            # DECISION DATA
            # ==================================================

            classification = decision.get(
                "classification",
                "N/A"
            )

            risk_score = decision.get(
                "risk_score",
                financial_risk.get(
                    "risk_score",
                    "N/A"
                )
            )

            confidence = decision.get(
                "confidence_level",
                0
            )

            risk_level = financial_risk.get(
                "risk_level",
                financial_risk.get(
                    "risk_category",
                    "N/A"
                )
            )


            # ==================================================
            # AI LOAN DECISION
            # ==================================================

            st.markdown(
                '<div class="section-title">'
                'AI Loan Decision'
                '</div>',
                unsafe_allow_html=True
            )


            if classification == "APPROVE":

                st.markdown(
                    '<div class="decision-box approve">'
                    'APPROVE'
                    '</div>',
                    unsafe_allow_html=True
                )

            elif classification == "REJECT":

                st.markdown(
                    '<div class="decision-box reject">'
                    'REJECT'
                    '</div>',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    '<div class="decision-box review">'
                    'REVIEW'
                    '</div>',
                    unsafe_allow_html=True
                )


            # ==================================================
            # TOP METRICS
            # ==================================================

            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "Risk Score",
                    risk_score
                )


            with col2:

                if isinstance(
                    confidence,
                    (int, float)
                ):

                    confidence_display = (
                        f"{confidence * 100:.0f}%"
                    )

                else:

                    confidence_display = confidence

                st.metric(
                    "Confidence",
                    confidence_display
                )


            with col3:

                st.metric(
                    "Risk Level",
                    risk_level
                )


            with col4:

                st.metric(
                    "Employment",
                    application_data.get(
                        "employment_type",
                        employment_type
                    )
                )


            # ==================================================
            # APPLICANT INFORMATION
            # ==================================================

            st.markdown(
                '<div class="section-title">'
                'Applicant Information'
                '</div>',
                unsafe_allow_html=True
            )


            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    f"**Applicant ID:** "
                    f"{application_data.get('applicant_id', applicant_id)}"
                )

                st.write(
                    f"**Name:** "
                    f"{application_data.get('name', name)}"
                )

                st.write(
                    f"**Age:** "
                    f"{application_data.get('age', age)}"
                )

                st.write(
                    f"**Location:** "
                    f"{application_data.get('location', location)}"
                )


            with col2:

                income_value = application_data.get(
                    "income",
                    income
                )

                loan_value = application_data.get(
                    "loan_amount",
                    loan_amount
                )

                debt_value = application_data.get(
                    "debt_obligations",
                    debt_obligations
                )

                tenure_value = application_data.get(
                    "loan_tenure",
                    loan_tenure
                )

                st.write(
                    f"**Annual Income:** "
                    f"₹{income_value:,.0f}"
                )

                st.write(
                    f"**Loan Amount:** "
                    f"₹{loan_value:,.0f}"
                )

                st.write(
                    f"**Loan Tenure:** "
                    f"{tenure_value} years"
                )

                st.write(
                    f"**Debt Obligations:** "
                    f"₹{debt_value:,.0f}"
                )


            # ==================================================
            # FINANCIAL RISK
            # ==================================================

            st.markdown(
                '<div class="section-title">'
                '📊 Financial Risk Assessment'
                '</div>',
                unsafe_allow_html=True
            )


            financial_risk_score = financial_risk.get(
                "risk_score",
                "N/A"
            )

            credit_score_risk = financial_risk.get(
                "credit_score_risk",
                "N/A"
            )

            loan_amount_risk = financial_risk.get(
                "loan_amount_risk",
                "N/A"
            )

            dti = financial_risk.get(
                "debt_to_income_ratio",
                "N/A"
            )

            anomaly = financial_risk.get(
                "anomaly_detected",
                False
            )


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "Risk Score",
                    financial_risk_score
                )


            with col2:

                st.metric(
                    "Credit Score Risk",
                    credit_score_risk
                )


            with col3:

                if isinstance(
                    dti,
                    (int, float)
                ):

                    dti_display = f"{dti * 100:.0f}%"

                else:

                    dti_display = dti

                st.metric(
                    "Debt-to-Income",
                    dti_display
                )


            with col4:

                st.metric(
                    "Anomaly",
                    "Detected"
                    if anomaly
                    else "None"
                )


            st.write(
                f"**Loan Amount Risk:** "
                f"{loan_amount_risk}"
            )


            # ==================================================
            # KEY DECISION FACTORS
            # ==================================================

            st.markdown(
                '<div class="section-title">'
                '🔍 Key Decision Factors'
                '</div>',
                unsafe_allow_html=True
            )


            factors = decision.get(
                "key_decision_factors",
                []
            )


            if factors:

                for factor in factors:

                    st.markdown(
                        f"• {factor}"
                    )

            else:

                st.info(
                    "No decision factors available."
                )


            # ==================================================
            # AI REASONING
            # ==================================================

            reasoning = financial_risk.get(
                "reasoning",
                decision.get(
                    "reasoning",
                    ""
                )
            )


            if reasoning:

                st.markdown(
                    '<div class="section-title">'
                    'AI Risk Reasoning'
                    '</div>',
                    unsafe_allow_html=True
                )

                with st.expander(
                    "Why was this decision made?"
                ):

                    st.write(reasoning)


            # ==================================================
            # COMPLIANCE
            # ==================================================

            st.markdown(
                '<div class="section-title">'
                '🛡️ Compliance Result'
                '</div>',
                unsafe_allow_html=True
            )


            action = compliance.get(
                "action_taken",
                "N/A"
            )

            notification = compliance.get(
                "notification_sent",
                False
            )

            case_id = compliance.get(
                "case_id",
                "N/A"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Action",
                    action
                )


            with col2:

                st.metric(
                    "Notification",
                    "Sent"
                    if notification
                    else "Not Sent"
                )


            with col3:

                st.metric(
                    "Case ID",
                    case_id
                )


            # ==================================================
            # OPTIONAL RAW RESPONSE
            # ==================================================

            # Keep this commented during the demo.
            # You can uncomment it if evaluator wants
            # to see the complete LangGraph response.

            with st.expander("View Complete API Response"):
                st.json(result)


        # ==================================================
        # API ERROR
        # ==================================================

        else:

            st.error(
                f"FastAPI returned error "
                f"{response.status_code}"
            )

            st.write(
                response.text
            )


    # ==================================================
    # CONNECTION ERROR
    # ==================================================

    except requests.exceptions.Timeout:

        st.error(
            "⏱️ The loan processing is taking longer "
            "than expected. Please try again."
        )


    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to FastAPI. "
            "Please make sure your FastAPI server is running."
        )


    except Exception as e:

        st.error(
            f"Unexpected error: {e}"
        )