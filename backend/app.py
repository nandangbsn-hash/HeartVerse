"""FastAPI service for HeartVerse decision-support inference."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Optional

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field

from datasets.prepare_datasets import FEATURE_COLUMNS
from ml.train import CardiovascularRiskModel


class PatientInput(BaseModel):
    age: int = Field(ge=18, le=120)
    sex: str = Field(pattern="^(M|F)$")
    bp_systolic: float = Field(ge=70, le=260)
    bp_diastolic: float = Field(ge=40, le=160)
    cholesterol: float = Field(ge=80, le=500)
    resting_hr: float = Field(ge=30, le=220)
    bmi: float = Field(ge=10, le=60)
    ecg_regularity: float = Field(ge=0.0, le=1.0)
    heart_failure_flag: int = Field(ge=0, le=1)
    stress_score: int = Field(ge=1, le=5)
    fatigue_score: int = Field(ge=1, le=5)


class CheckInInput(BaseModel):
    baseline_risk: float = Field(ge=0, le=1)
    stress_score: int = Field(ge=1, le=5)
    fatigue_score: int = Field(ge=1, le=5)
    breathlessness: bool
    chest_discomfort: bool


app = FastAPI(title="HeartVerse API", version="0.1.0")
model: Optional[CardiovascularRiskModel] = None


def _to_features(payload: PatientInput) -> np.ndarray:
    sex_male = 1 if payload.sex == "M" else 0
    data = {
        "age": payload.age,
        "sex_male": sex_male,
        "bp_systolic": payload.bp_systolic,
        "bp_diastolic": payload.bp_diastolic,
        "cholesterol": payload.cholesterol,
        "resting_hr": payload.resting_hr,
        "bmi": payload.bmi,
        "ecg_regularity": payload.ecg_regularity,
        "hf_history": payload.heart_failure_flag,
        "stress_score": payload.stress_score,
        "fatigue_score": payload.fatigue_score,
    }
    data["pulse_pressure"] = data["bp_systolic"] - data["bp_diastolic"]
    data["rate_pressure_product"] = data["bp_systolic"] * data["resting_hr"]
    data["metabolic_stress_proxy"] = data["bmi"] * data["stress_score"]
    return np.array([[data[col] for col in list(FEATURE_COLUMNS) + ["pulse_pressure", "rate_pressure_product", "metabolic_stress_proxy"]]], dtype=float)


def _explain(risk: float, contractility: float, stiffness: float) -> str:
    band = "low" if risk < 0.3 else "moderate" if risk < 0.6 else "elevated"
    return (
        f"Decision-support estimate suggests {band} near-term cardiovascular strain "
        f"(risk={risk:.2f}). Contractility proxy={contractility:.2f}, "
        f"wall stiffness proxy={stiffness:.2f}. This is educational and not a diagnosis."
    )


@app.on_event("startup")
def startup():
    global model
    model = CardiovascularRiskModel(model_type="xgboost")
    model_path = Path("ml/models/risk_model.pkl")
    if model_path.exists():
        with model_path.open("rb") as f:
            payload = pickle.load(f)
        model.model = payload["model"]
        model.feature_names = payload.get("feature_names", [])


@app.get("/")
def root():
    return {"service": "HeartVerse", "regulatory_position": "research and decision-support only"}


@app.post("/api/assess-cardiovascular-health")
def assess(patient: PatientInput):
    assert model is not None
    features = _to_features(patient)
    out = model.predict_physiological_params(features)
    risk = float(out["risk"][0])
    contractility = float(out["contractility"][0])
    stiffness = float(out["wall_stiffness"][0])
    rhythm = float(out["rhythm_stability"][0])
    return {
        "risk_score": risk,
        "contractility": contractility,
        "wall_stiffness": stiffness,
        "rhythm_stability": rhythm,
        "confidence_interval": [max(0.0, risk - 0.08), min(1.0, risk + 0.08)],
        "explanation": _explain(risk, contractility, stiffness),
        "disclaimer": "Not a diagnostic or therapeutic medical device.",
    }


@app.post("/api/process-daily-checkin")
def process_checkin(checkin: CheckInInput):
    symptom_penalty = 0.03 * (checkin.stress_score - 3) + 0.03 * (checkin.fatigue_score - 3)
    if checkin.breathlessness:
        symptom_penalty += 0.05
    if checkin.chest_discomfort:
        symptom_penalty += 0.06
    adjusted = float(np.clip(checkin.baseline_risk + symptom_penalty, 0.0, 1.0))
    return {
        "adjusted_risk": adjusted,
        "delta": adjusted - checkin.baseline_risk,
        "guidance": "If symptoms worsen or persist, seek qualified clinical evaluation.",
    }
