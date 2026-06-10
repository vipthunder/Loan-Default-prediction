import streamlit as st
import requests

# -----------------------------
# Configuration
# -----------------------------
API_URL = "https://loan-default-prediction-production.up.railway.app/predict"

st.set_page_config(
    page_title="Loan Default Risk Predictor",
    page_icon="🏦",
    layout="centered"
)

# -----------------------------
# Header
# -----------------------------
st.title("🏦 Loan Default Risk Prediction")

st.markdown(
    """
    Enter applicant details below to estimate the probability of loan default
    using an XGBoost machine learning model.
    """
)

# -----------------------------
# Input Fields
# -----------------------------
person_age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=25
)

person_income = st.number_input(
    "Annual Income",
    min_value=1000.0,
    value=50000.0
)

loan_amnt = st.number_input(
    "Loan Amount",
    min_value=100.0,
    value=10000.0
)

loan_int_rate = st.number_input(
    "Interest Rate (%)",
    min_value=0.0,
    max_value=50.0,
    value=12.5
)

person_home_ownership = st.selectbox(
    "Home Ownership",
    ["RENT", "OWN", "MORTGAGE", "OTHER"]
)

loan_intent = st.selectbox(
    "Loan Intent",
    [
        "EDUCATION",
        "MEDICAL",
        "VENTURE",
        "PERSONAL",
        "HOMEIMPROVEMENT",
        "DEBTCONSOLIDATION"
    ]
)

loan_grade = st.selectbox(
    "Loan Grade",
    ["A", "B", "C", "D", "E", "F", "G"]
)

cb_person_default_on_file = st.selectbox(
    "Previous Default",
    ["N", "Y"]
)

person_emp_length = st.number_input(
    "Employment Length (Years)",
    min_value=0.0,
    value=2.0
)

cb_person_cred_hist_length = st.number_input(
    "Credit History Length (Years)",
    min_value=0.0,
    value=4.0
)

# Derived Feature
loan_percent_income = (
    loan_amnt / person_income
    if person_income > 0
    else 0
)

# -----------------------------
# Prediction Button
# -----------------------------
if st.button("Predict Risk", use_container_width=True):

    payload = {
        "person_age": person_age,
        "person_income": person_income,
        "person_home_ownership": person_home_ownership,
        "person_emp_length": person_emp_length,
        "loan_intent": loan_intent,
        "loan_grade": loan_grade,
        "loan_amnt": loan_amnt,
        "loan_int_rate": loan_int_rate,
        "loan_percent_income": loan_percent_income,
        "cb_person_default_on_file": cb_person_default_on_file,
        "cb_person_cred_hist_length": cb_person_cred_hist_length,
        "person_emp_length_missing": int(person_emp_length == 0)
    }

    try:

        with st.spinner("Generating prediction..."):

            response = requests.post(
                API_URL,
                json=payload,
                timeout=30
            )

        if response.status_code == 200:

            result = response.json()

            risk = result["risk_category"]
            probability = float(result["default_probability"])

            st.success("Prediction Generated Successfully")

            st.subheader(" Prediction Result")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Default Probability",
                    f"{probability:.2%}"
                )

            with col2:
                st.metric(
                    "Risk Category",
                    risk
                )

            # st.write("### Risk Score")
            # st.progress(min(max(probability, 0.0), 1.0))

            if risk == "Low Risk":
                st.success(
                    " Applicant is classified as Low Risk."
                )

            elif risk == "Medium Risk":
                st.warning(
                    " Applicant is classified as Medium Risk."
                )

            else:
                st.error(
                    " Applicant is classified as High Risk."
                )

        else:
            st.error(
                f"API Error: {response.status_code}"
            )
            st.write(response.text)

    except requests.exceptions.ConnectionError:
        st.error(
            "Unable to connect to the prediction API."
        )

    except requests.exceptions.Timeout:
        st.error(
            "The request timed out."
        )

    except requests.exceptions.RequestException as e:
        st.error(
            f"Request failed: {str(e)}"
        )

    except Exception as e:
        st.error(
            f"Unexpected error: {str(e)}"
        )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.caption(
    """
    Built with XGBoost, FastAPI, Railway, and Streamlit.
    """
)
