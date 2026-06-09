from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()


model = joblib.load("models/xgboost_model.pkl")
preprocessor = joblib.load("models/preprocessor.pkl")

class LoanApplication(BaseModel):
    person_age: int
    person_income: float
    person_home_ownership: str
    person_emp_length: float
    loan_intent: str
    loan_grade: str
    loan_amnt: float
    loan_int_rate: float
    loan_percent_income: float
    cb_person_default_on_file: str
    cb_person_cred_hist_length: float
    person_emp_length_missing: int

@app.get("/")
def home():
    return {"message": "Loan Default Prediction API Running"}

@app.post("/predict")
def predict(data: LoanApplication):

    df = pd.DataFrame([data.dict()])

    X = preprocessor.transform(df)

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]

    risk = "High Risk" if prediction == 1 else "Low Risk"

    return {
        "risk_category": risk,
        "default_probability": round(float(probability), 4)
    }