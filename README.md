# HeartVerse — Digital Cardiovascular Twin + AI Translator + Daily Check-In

**Educational use only. Not a medical device or diagnostic tool.**

## Project Overview

HeartVerse is a web-based application that creates a patient-specific 3D digital heart twin powered by machine learning. It explains cardiovascular health in simple language using an AI agent and includes a daily patient check-in system for tracking symptom trends.

## Core Features

1. **Digital Heart Twin (3D + Simulation)**
   - Parametric 3D heart model (left & right ventricles)
   - Animated cardiac cycle (systole/diastole)
   - Color-mapped strain/stress visualization (green→yellow→red)
   - Data-driven, not random parameters

2. **Machine Learning Layer**
   - Tabular cardiovascular risk model (XGBoost/LightGBM)
   - ECG rhythm stability model
   - Outputs: Risk score, contractility, wall stiffness, rhythm regularity

3. **AI Cardio Translator Agent**
   - Plain-language explanations of cardiac status
   - Lifestyle implications (diet, activity, stress)
   - No medical diagnosis or medication advice

4. **Daily Patient Check-In**
   - Fatigue (1–5), chest discomfort (Y/N), breathlessness (Y/N), stress (1–5)
   - Symptom trend scoring
   - Short-term risk adjustment
   - Influences AI explanation tone

5. **Patient Cardiovascular Portfolio**
   - 3D heart visualization
   - Risk score + explanation
   - Check-in history
   - Trend visualization
   - AI-generated summary

## Technical Stack

### Backend
- **FastAPI** (Python) - ML inference, simulation parameters
- **XGBoost/LightGBM** - Risk prediction
- **SHAP** - Model interpretability
- **pandas, numpy** - Data processing

### Frontend
- **Next.js** - React framework
- **Three.js** - 3D heart rendering
- **Tailwind CSS** - UI styling

### ML Stack
- **scikit-learn, XGBoost, LightGBM** - Model training
- **PyTorch** - Optional ECG models
- **SHAP** - Feature importance

## Project Structure

```
heartverse/
├── backend/              # FastAPI server
│   ├── app.py           # Main FastAPI app
│   ├── models/          # ML model serving
│   ├── simulation/       # Heart simulation engine
│   └── requirements.txt
├── frontend/            # Next.js React app
│   ├── pages/
│   ├── components/      # 3D heart, check-in forms
│   ├── styles/
│   └── package.json
├── ml/                  # ML pipeline & models
│   ├── train.py        # Model training
│   ├── evaluate.py     # AUROC, calibration, sensitivity
│   ├── models/         # Trained model artifacts
│   └── features.py     # Feature engineering
├── datasets/            # Cardiovascular data
│   └── README.md        # Data source documentation
├── docs/                # Documentation & evaluation reports
└── README.md
```

## Setup Instructions

### Backend Setup

1. Create Python virtual environment:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run ML training pipeline first:
```bash
cd ../ml
python train.py
```

4. Start FastAPI server:
```bash
cd ../backend
uvicorn app:app --reload
```

### Frontend Setup

1. Install Node dependencies:
```bash
cd frontend
npm install
```

2. Run development server:
```bash
npm run dev
```

## System Flow

```
Patient Input (Age, Sex, BP, Cholesterol, ECG, HF indicators)
    ↓
Feature Engineering
    ↓
ML Risk & Physiology Models
    ↓
Heart Simulation Parameters (contractility, wall stiffness, rhythm)
    ↓
3D Heart Rendering + Animation
    ↓
AI Explanation Agent
    ↑
Daily Check-In Feedback Loop
```

## Evaluation Metrics

- **AUROC** for ML models
- **Calibration plot** for risk scores
- **Sensitivity analysis** for parameter changes
- **Readability score** for AI explanations

## Ethical & Safety Constraints

- ⚠️ **Disclaimer**: Educational use only. Not a medical device.
- No diagnosis, treatment advice, or medication names
- Explainable AI outputs (SHAP values)
- Clear uncertainty communication

## Success Criteria

- ✅ Different patients generate visibly different 3D hearts
- ✅ Input changes affect heart behavior
- ✅ AI explanations match heart visuals
- ✅ Daily check-ins influence system outputs
- ✅ Reproducible ML pipeline with fixed seeds

## Datasets Used

[To be populated after data collection]

## Author & License

HeartVerse - Computational Health Demonstration Project

---

**Disclaimer**: This tool is for educational and demonstration purposes only. It is not a medical device and should not be used for clinical decision-making.
