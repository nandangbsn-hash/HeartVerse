# HeartVerse Quick Start Guide

## Prerequisites

- Python 3.9+
- Node.js 16+ (for frontend)
- pip and npm

## Quick Start (5 minutes)

### 1. Set Up Python Environment

```bash
# Navigate to project
cd heartverse

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Data & Train ML Models

```bash
# Run complete ML pipeline
python run_ml_pipeline.py
```

This will:
- ✅ Download/generate cardiovascular datasets
- ✅ Create feature engineering
- ✅ Train XGBoost risk model
- ✅ Evaluate model (AUROC, calibration)
- ✅ Generate evaluation visualizations
- ✅ Save trained models

**Output**: 
- Trained model at `ml/models/xgboost_risk_model.pkl`
- Evaluation plots at `ml/evaluation_results/`
- Model metadata at `ml/models/metadata.json`

### 3. Start Backend Server

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Server runs at: `http://localhost:8000`

**Test the API**:
```bash
# Open in browser or curl:
curl http://localhost:8000

# Assess patient cardiovascular health:
curl -X POST http://localhost:8000/api/assess-cardiovascular-health \
  -H "Content-Type: application/json" \
  -d '{
    "age": 55,
    "sex": "M",
    "bp_systolic": 140,
    "bp_diastolic": 85,
    "cholesterol": 220,
    "ecg_regularity": 0.8,
    "heart_failure_flag": 0
  }'
```

**API Documentation**: Visit `http://localhost:8000/docs` (Swagger UI)

### 4. Start Frontend (Optional)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:3000`

---

## Project Structure

```
heartverse/
├── ml/                          # ML models & training
│   ├── features.py             # Feature engineering
│   ├── train.py               # Model training
│   ├── evaluate.py            # Evaluation & viz
│   ├── models/                # Trained models
│   └── evaluation_results/    # AUROC, calibration plots
│
├── backend/                    # FastAPI server
│   ├── app.py                 # Main API
│   └── requirements.txt
│
├── datasets/                   # Cardiovascular data
│   ├── synthetic_heart_disease.csv
│   └── prepare_datasets.py
│
├── run_ml_pipeline.py         # Orchestration script
├── requirements.txt           # All Python deps
└── README.md
```

---

## Key Files

### ML Pipeline

| File | Purpose |
|------|---------|
| `ml/features.py` | Data loading, feature engineering, synthetic data generation |
| `ml/train.py` | XGBoost/LightGBM models, physiological parameter prediction |
| `ml/evaluate.py` | AUROC, calibration curves, sensitivity analysis |
| `datasets/prepare_datasets.py` | Download UCI dataset, generate synthetic data |

### Backend API

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Root info |
| `/health` | GET | Health check |
| `/api/assess-cardiovascular-health` | POST | Get risk + parameters |
| `/api/heart-simulation-params` | POST | 3D visualization params |
| `/api/process-daily-checkin` | POST | Symptom tracking |
| `/api/model-info` | GET | ML model metadata |

### Key Functions

**Feature Engineering** (`ml/features.py`):
```python
loader = CardiovascularDataLoader()
data = loader.prepare_data('datasets/synthetic_heart_disease.csv')
# Returns: X_train, X_test, y_train, y_test, feature_names
```

**Model Training** (`ml/train.py`):
```python
model = CardiovascularRiskModel(model_type='xgboost')
model.train(X_train, y_train, X_val, y_val)
params = model.predict_physiological_params(X_test)
# Returns: contractility, wall_stiffness, rhythm_regularity, risk_score
```

**Model Evaluation** (`ml/evaluate.py`):
```python
evaluator = ModelEvaluator(model)
auroc_results = evaluator.evaluate_auroc(X_test, y_test)
sensitivity = evaluator.sensitivity_analysis(X_baseline, feature_names)
```

---

## Sample Patient Request

```bash
curl -X POST http://localhost:8000/api/assess-cardiovascular-health \
  -H "Content-Type: application/json" \
  -d '{
    "age": 65,
    "sex": "F",
    "bp_systolic": 145,
    "bp_diastolic": 88,
    "cholesterol": 240,
    "ecg_regularity": 0.75,
    "heart_failure_flag": 1
  }'
```

**Response** (example):
```json
{
  "risk_score": 0.68,
  "contractility": 0.52,
  "wall_stiffness": 0.65,
  "rhythm_regularity": 0.75,
  "interpretation": "Your heart is under noticeable strain, similar to climbing stairs while carrying a backpack..."
}
```

---

## Evaluation Outputs

After running `python run_ml_pipeline.py`, check:

1. **AUROC Curve** (`ml/evaluation_results/roc_curve.png`)
   - Shows discrimination ability
   - Target: AUROC > 0.7

2. **Calibration Curve** (`ml/evaluation_results/calibration_curve.png`)
   - Shows probability calibration
   - Target: Points close to diagonal

3. **Sensitivity Analysis** (`ml/evaluation_results/sensitivity_analysis.png`)
   - Shows which features affect heart parameters most

4. **Risk Distribution** (`ml/evaluation_results/risk_distribution.png`)
   - Compares actual vs predicted risk

---

## Common Issues

### "Model not loaded" error
**Solution**: Run `python run_ml_pipeline.py` first to train models

### Missing datasets
**Solution**: `python datasets/prepare_datasets.py` generates synthetic data

### CORS errors
**Already configured** in `backend/app.py`

### Port already in use
**Solution**: 
```bash
# Use different port
uvicorn backend.app:app --port 8001
```

---

## Next Steps

1. ✅ **Complete ML pipeline** (you are here)
2. 🚀 **Integrate 3D heart visualization** (Three.js)
3. 🚀 **Build React frontend** (Next.js)
4. 🚀 **Add daily check-in UI**
5. 🚀 **Deploy to cloud**

---

## Disclaimer

⚠️ **Educational Use Only**

This tool is for demonstration and educational purposes only. It is NOT a medical device and should NOT be used for:
- Diagnosis
- Treatment planning
- Medical decision-making

Always consult qualified healthcare professionals for medical advice.

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **XGBoost Docs**: https://xgboost.readthedocs.io/
- **scikit-learn**: https://scikit-learn.org/
- **SHAP**: https://shap.readthedocs.io/

---

**Last Updated**: January 2026
