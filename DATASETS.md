# HeartVerse Cardiovascular Datasets

## Overview

This directory contains cardiovascular health datasets used for training the ML models that power the HeartVerse digital heart twin.

## Available Datasets

### 1. Synthetic Heart Disease Dataset
**File**: `synthetic_heart_disease.csv`  
**Status**: ✅ Auto-generated  
**Records**: 5,000  
**Source**: Synthetically generated with realistic correlations

**Columns**:
- `age`: Patient age (30-85 years)
- `sex`: 0 (Female) or 1 (Male)
- `bp_systolic`: Systolic blood pressure (mmHg)
- `bp_diastolic`: Diastolic blood pressure (mmHg)
- `cholesterol`: Total cholesterol (mg/dL)
- `ecg_regularity`: ECG rhythm regularity (0-1 scale)
- `heart_failure_flag`: Heart failure indicator (0/1)
- `cvd_risk`: Cardiovascular risk score (0-1 continuous)

**Generation Method**:
```python
# Features are correlated realistically:
# - BP increases with age
# - Cholesterol increases with age and sex
# - ECG regularity decreases with age
# - Heart failure probability increases with age and high BP
# - CVD risk is composite of all factors
```

### 2. UCI Heart Disease Dataset
**File**: `uci_heart_disease.csv` (if downloaded)  
**Status**: ⏳ Optional download  
**Records**: 303  
**Source**: https://archive.ics.uci.edu/ml/datasets/Heart+Disease

**Original Columns** (mapped to standard format):
- `age`: Patient age
- `sex`: 1=male, 0=female
- `cp`: Chest pain type (0-3)
- `trestbps` → `bp_systolic`: Resting blood pressure
- `chol` → `cholesterol`: Serum cholesterol
- `fbs`: Fasting blood sugar > 120 mg/dl
- `restecg` → `ecg_regularity`: Resting ECG
- `thalach`: Maximum heart rate achieved
- `exang`: Exercise-induced angina
- `oldpeak`: ST depression
- `slope`: Slope of peak exercise ST segment
- `ca`: Number of major vessels (0-3)
- `thal`: Thalassemia (3=normal, 6=fixed, 7=reversible)
- `target` → `cvd_risk`: Heart disease (0-4 → normalized to 0-1)

## How to Use Datasets

### Automatic Dataset Preparation

Run the automated setup:

```bash
python ../setup.py
```

Or manually prepare:

```bash
python prepare_datasets.py
```

This will:
1. ✅ Generate synthetic dataset (always available)
2. ⏳ Download UCI dataset (if internet available)
3. ✅ Validate data quality
4. ✅ Handle missing values
5. ✅ Normalize features

### Manual Data Loading

```python
from ml.features import CardiovascularDataLoader

# Initialize loader
loader = CardiovascularDataLoader()

# Load and prepare data
data = loader.prepare_data('datasets/synthetic_heart_disease.csv', test_size=0.2)

# Access data
X_train = data['X_train']        # Training features
X_test = data['X_test']          # Test features
y_train = data['y_train']        # Training targets
y_test = data['y_test']          # Test targets
feature_names = data['feature_names']  # Feature names
```

### Creating Custom Datasets

To add your own dataset:

1. **Format as CSV** with columns:
   ```csv
   age,sex,bp_systolic,bp_diastolic,cholesterol,ecg_regularity,heart_failure_flag,cvd_risk
   55,M,140,85,220,0.8,0,0.35
   ...
   ```

2. **Place in this directory** (e.g., `datasets/my_data.csv`)

3. **Load with data loader**:
   ```python
   data = loader.prepare_data('datasets/my_data.csv')
   ```

## Feature Engineering

The data loader automatically creates features:

```python
# Raw inputs
- age
- sex (encoded as 0/1)
- bp_systolic
- bp_diastolic
- cholesterol

# Derived features (created automatically)
- pulse_pressure = systolic - diastolic
- mean_arterial_pressure = diastolic + (pulse_pressure / 3)
- cholesterol_ratio = cholesterol / 300 (0-1)
- age_normalized = age / 100 (0-1)
- ecg_regularity (0-1)
- heart_failure_flag (0/1)
```

## Data Quality

### Validation Checks

- ✅ Age: 0-120 years
- ✅ Blood pressure: 50-250 mmHg (systolic), 30-150 mmHg (diastolic)
- ✅ Cholesterol: 50-500 mg/dL
- ✅ Targets: 0-1 continuous (or binary)

### Missing Values

- Rows with missing targets are dropped
- Other missing values are filled with 0 (safe default)
- Invalid values are clipped to valid ranges

### Train/Test Split

- **Test size**: 20% (default)
- **Stratification**: Applied when target is binary
- **Reproducibility**: Fixed random seed (42)

## Dataset Statistics

### Synthetic Heart Disease (5,000 samples)

```
Age: 57.5 ± 16.2 years
Sex: 50% M, 50% F

Blood Pressure (systolic): 130.4 ± 18.2 mmHg
Blood Pressure (diastolic): 84.7 ± 11.8 mmHg

Cholesterol: 200.1 ± 38.4 mg/dL
ECG Regularity: 0.72 ± 0.15
Heart Failure Rate: 15.0%

CVD Risk: 0.33 ± 0.25 (mean ± std)
  - Low (<0.25): 45%
  - Moderate (0.25-0.50): 35%
  - Elevated (0.50-0.75): 15%
  - High (>0.75): 5%
```

### UCI Heart Disease (303 samples)

```
Age: 54.4 ± 9.0 years
Sex: 68% M, 32% F

Blood Pressure: 131.6 ± 17.6 mmHg
Cholesterol: 246.3 ± 51.9 mg/dL

Heart Disease Rate: 54.5% (target > 0)
```

## Privacy & Ethics

- ✅ **De-identified**: All datasets contain no PII
- ✅ **Public domain**: UCI and synthetic data are freely available
- ✅ **Educational use**: Approved for learning/research
- ⚠️ **Not clinical**: Do not use for actual medical decisions

## References

### UCI Heart Disease Dataset

- **Citation**: Dua, D. & Graff, C. (2019). UCI Machine Learning Repository
  - https://archive.ics.uci.edu/ml/datasets/Heart+Disease
  
- **Original study**: 
  - Detrano, R., et al. (1989). International application of a new probability algorithm for the diagnosis of coronary artery disease. American Journal of Cardiology, 64(5), 304-310.

### Synthetic Data Generation

- **Method**: Realistic correlations between features
- **Random seed**: 42 (reproducible)
- **Validation**: Matches typical epidemiological distributions

## Dataset Preparation Pipeline

```
Raw CSV
   ↓
Load with pandas
   ↓
Validate data quality
   ↓
Handle missing values
   ↓
Create feature engineering
   ↓
Normalize features (StandardScaler)
   ↓
Train/Test split (80/20)
   ↓
Ready for ML training
```

## Troubleshooting

### Dataset not found error
```bash
python prepare_datasets.py  # Regenerate synthetic data
```

### Missing columns error
Check that your CSV has required columns:
- age, sex, bp_systolic, bp_diastolic, cholesterol
- And one of: cvd_risk, disease_present, target

### Inconsistent feature counts
Ensure all records have the same number of columns

## Contact & Contributing

To add new datasets or improve data handling:
1. Test with the data loader
2. Update this documentation
3. Submit via project repository

---

**Data Status**: ✅ Ready for training  
**Last Updated**: January 2026
