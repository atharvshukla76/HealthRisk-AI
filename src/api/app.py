from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

model = joblib.load('notebooks/models/healthrisk_xgboost.pkl')
pipeline = joblib.load('notebooks/models/preprocessing_pipeline.pkl')

app = FastAPI(title="HealthRisk AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    age: float
    gender: str
    weight: float
    bp: str
    hr: float
    smoker: str

@app.get("/")
def health_check():
    return {"status": "HealthRisk API is running"}

@app.post("/predict")
def predict_risk(patient: PatientData):
    # Parse blood pressure string (e.g., "120/80" -> 120.0)
    try:
        systolic_bp = float(patient.bp.split('/')[0])
    except:
        systolic_bp = 120.0 # Default fallback

    # Create a DataFrame that perfectly matches what the pipeline expects
    input_df = pd.DataFrame([{
        'age': patient.age,
        'gender': patient.gender,
        'weight': patient.weight,
        'systolic_bp': systolic_bp,
        'hr': patient.hr,
        'smoker': patient.smoker
    }])
    
    clean_data = pipeline.transform(input_df)
    risk_probability = model.predict_proba(clean_data)[0][1]
    
    return {
        "risk_probability": float(risk_probability),
        "high_risk": bool(risk_probability > 0.70)
    }