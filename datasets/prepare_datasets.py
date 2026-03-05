"""Schema-compatible dataset preparation for HeartVerse.

Implements local synthetic data generation when external datasets are unavailable.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

SEED = 42


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    rows: int


DATASET_SPECS = (
    DatasetSpec("synthetic_cardiovascular", 5000),
    DatasetSpec("mimiciv_schema_compatible", 4000),
    DatasetSpec("eicu_schema_compatible", 3500),
    DatasetSpec("ukbiobank_schema_compatible", 3000),
    DatasetSpec("ptbxl_schema_compatible", 2500),
    DatasetSpec("framingham_schema_compatible", 2000),
)


FEATURE_COLUMNS = [
    "age",
    "sex_male",
    "bp_systolic",
    "bp_diastolic",
    "cholesterol",
    "resting_hr",
    "bmi",
    "ecg_regularity",
    "hf_history",
    "stress_score",
    "fatigue_score",
]


TARGET_COLUMN = "risk_target"


def _generate_dataframe(n_rows: int, rng: np.random.Generator) -> pd.DataFrame:
    age = rng.integers(30, 90, size=n_rows)
    sex_male = rng.integers(0, 2, size=n_rows)
    bp_systolic = rng.normal(120 + 0.45 * (age - 50), 12, size=n_rows).clip(85, 220)
    bp_diastolic = rng.normal(75 + 0.12 * (age - 50), 8, size=n_rows).clip(50, 130)
    cholesterol = rng.normal(190 + 0.7 * (age - 50), 28, size=n_rows).clip(100, 420)
    resting_hr = rng.normal(72 + 0.08 * (age - 50), 10, size=n_rows).clip(45, 140)
    bmi = rng.normal(27, 4.8, size=n_rows).clip(16, 50)
    ecg_regularity = rng.normal(0.88 - 0.0014 * (age - 50), 0.07, size=n_rows).clip(0.45, 1.0)
    hf_history = (rng.random(n_rows) < (0.06 + (age - 30) / 850)).astype(int)
    stress_score = rng.integers(1, 6, size=n_rows)
    fatigue_score = rng.integers(1, 6, size=n_rows)

    raw_risk = (
        0.012 * (age - 30)
        + 0.007 * (bp_systolic - 110)
        + 0.006 * (cholesterol - 170)
        + 0.25 * hf_history
        + 0.12 * (1 - ecg_regularity)
        + 0.03 * (stress_score - 3)
        + 0.025 * (fatigue_score - 3)
    )
    risk_target = (1 / (1 + np.exp(-(raw_risk - 1.2))) + rng.normal(0, 0.03, size=n_rows)).clip(0, 1)

    return pd.DataFrame(
        {
            "age": age,
            "sex_male": sex_male,
            "bp_systolic": bp_systolic,
            "bp_diastolic": bp_diastolic,
            "cholesterol": cholesterol,
            "resting_hr": resting_hr,
            "bmi": bmi,
            "ecg_regularity": ecg_regularity,
            "hf_history": hf_history,
            "stress_score": stress_score,
            "fatigue_score": fatigue_score,
            TARGET_COLUMN: risk_target,
        }
    )


def prepare_all_datasets(output_dir: str | Path | None = None) -> Dict[str, Path]:
    """Create schema-compatible local datasets for ML development."""
    base = Path(output_dir) if output_dir else Path(__file__).resolve().parent
    base.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(SEED)
    outputs: Dict[str, Path] = {}
    for spec in DATASET_SPECS:
        df = _generate_dataframe(spec.rows, rng)
        out_path = base / f"{spec.name}.csv"
        df.to_csv(out_path, index=False)
        outputs[spec.name] = out_path

    return outputs


if __name__ == "__main__":
    files = prepare_all_datasets()
    for name, path in files.items():
        print(f"{name}: {path}")
