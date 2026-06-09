import streamlit as st
import requests

st.title("🏦 Loan Default Risk Predictor")

age = st.number_input("Age", min_value=18, max_value=100, value=25)

income = st.number_input(
    "Annual Income",
    min_value=0,
    value=50000
)

home = st.selectbox(
    "Home Ownership",
    ["RENT", "OWN", "MORTGAGE", "OTHER"]
)

emp_length = st.number_input(
    "Employment Length (Years)",
    min_value=0.0,
    value=2.0
)

intent = st.selectbox(
    "Loan Intent",
    [
        "PERSONAL",
        "EDUCATION",
        "MEDICAL",
        "VENTURE",
        "HOMEIMPROVEMENT",
        "DEBTCONSOLIDATION"
    ]
)

grade = st.selectbox(
    "Loan Grade",
    ["A", "B", "C", "D", "E", "F", "G"]
)

loan_amount = st.number_input(
    "Loan Amount",
    min_value=0,
    value=10000
)

interest_rate = st.number_input(
    "Interest Rate",
    min_value=0.0,
    value=12.5
)

loan_percent_income = st.number_input(
    "Loan Percent Income",
    min_value=0.0,
    value=0.2
)

default_history = st.selectbox(
    "Previous Default",
    ["N", "Y"]
)

credit_history = st.number_input(
    "Credit History Length",
    min_value=0,
    value=4
)

if st.button("Predict Risk"):

    payload = {
        "person_age": age,
        "person_income": income,
        "person_home_ownership": home,
        "person_emp_length": emp_length,
        "loan_intent": intent,
        "loan_grade": grade,
        "loan_amnt": loan_amount,
        "loan_int_rate": interest_rate,
        "loan_percent_income": loan_percent_income,
        "cb_person_default_on_file": default_history,
        "cb_person_cred_hist_length": credit_history,
        "person_emp_length_missing": 0
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload
    )

    result = response.json()

    st.subheader("Prediction Result")

    st.write(
        f"Risk Category: **{result['risk_category']}**"
    )

    st.write(
        f"Default Probability: **{result['default_probability']:.2%}**"
    )