"""Feature engineering for HeartVerse cardiovascular risk models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from datasets.prepare_datasets import FEATURE_COLUMNS, TARGET_COLUMN


@dataclass
class PreparedData:
    X_train: np.ndarray
    X_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    feature_names: List[str]


class CardiovascularDataLoader:
    """Loads schema-compatible cardiovascular datasets and engineers features."""

    def load_dataframe(self, path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        required = set(FEATURE_COLUMNS + [TARGET_COLUMN])
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        return df

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["pulse_pressure"] = out["bp_systolic"] - out["bp_diastolic"]
        out["rate_pressure_product"] = out["bp_systolic"] * out["resting_hr"]
        out["metabolic_stress_proxy"] = out["bmi"] * out["stress_score"]
        return out

    def prepare_data(self, path: str, test_size: float = 0.2, seed: int = 42) -> Dict[str, np.ndarray | List[str]]:
        df = self.engineer_features(self.load_dataframe(path))
        feature_names = [c for c in df.columns if c != TARGET_COLUMN]
        X = df[feature_names].to_numpy(dtype=float)
        y = df[TARGET_COLUMN].to_numpy(dtype=float)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=seed
        )
        return {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test,
            "feature_names": feature_names,
        }
