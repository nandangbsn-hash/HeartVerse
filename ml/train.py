"""Model training and inference logic for HeartVerse."""

from __future__ import annotations

import json
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, roc_auc_score, brier_score_loss
from sklearn.calibration import calibration_curve

try:
    from xgboost import XGBRegressor
except Exception:  # pragma: no cover
    XGBRegressor = None


class CardiovascularRiskModel:
    """Risk regression model with deterministic training."""

    def __init__(self, model_type: str = "xgboost", seed: int = 42):
        self.model_type = model_type
        self.seed = seed
        if model_type == "xgboost" and XGBRegressor is not None:
            self.model = XGBRegressor(
                n_estimators=180,
                max_depth=4,
                learning_rate=0.05,
                subsample=0.9,
                colsample_bytree=0.9,
                random_state=seed,
            )
        else:
            self.model = GradientBoostingRegressor(random_state=seed)
        self.feature_names: List[str] = []

    def train(self, X_train, y_train, X_val=None, y_val=None, feature_names=None) -> Dict[str, float]:
        self.feature_names = feature_names or []
        self.model.fit(X_train, y_train)
        train_pred = self.model.predict(X_train)
        metrics = {
            "train_rmse": float(np.sqrt(mean_squared_error(y_train, train_pred))),
            "train_mae": float(mean_absolute_error(y_train, train_pred)),
        }
        if X_val is not None and y_val is not None:
            val_pred = self.model.predict(X_val)
            metrics["val_rmse"] = float(np.sqrt(mean_squared_error(y_val, val_pred)))
            metrics["val_mae"] = float(mean_absolute_error(y_val, val_pred))
        return metrics

    def predict_risk(self, X) -> np.ndarray:
        return np.clip(self.model.predict(X), 0.0, 1.0)

    def predict_physiological_params(self, X) -> Dict[str, np.ndarray]:
        risk = self.predict_risk(X)
        contractility = np.clip(1.0 - 0.55 * risk, 0.2, 1.0)
        wall_stiffness = np.clip(0.2 + 0.7 * risk, 0.0, 1.0)
        rhythm_stability = np.clip(0.97 - 0.5 * risk, 0.2, 1.0)
        return {
            "risk": risk,
            "contractility": contractility,
            "wall_stiffness": wall_stiffness,
            "rhythm_stability": rhythm_stability,
        }

    def save(self, model_dir: str | Path = "ml/models") -> Path:
        out = Path(model_dir)
        out.mkdir(parents=True, exist_ok=True)
        model_path = out / "risk_model.pkl"
        with model_path.open("wb") as f:
            pickle.dump({"model": self.model, "feature_names": self.feature_names}, f)
        return model_path


@dataclass
class ModelEvaluator:
    model: CardiovascularRiskModel

    def evaluate_auroc(self, X_test, y_test):
        y_pred = self.model.predict_risk(X_test)
        y_bin = (y_test >= 0.5).astype(int)
        return {"auroc": float(roc_auc_score(y_bin, y_pred)), "fpr": [], "tpr": []}

    def evaluate_calibration(self, X_test, y_test):
        y_pred = self.model.predict_risk(X_test)
        y_bin = (y_test >= 0.5).astype(int)
        prob_true, prob_pred = calibration_curve(y_bin, y_pred, n_bins=10)
        return {
            "brier_score": float(brier_score_loss(y_bin, y_pred)),
            "prob_true": prob_true.tolist(),
            "prob_pred": prob_pred.tolist(),
        }

    def sensitivity_analysis(self, baseline_sample, feature_names):
        sample = np.array(baseline_sample, dtype=float)
        results = {}
        for i, feature in enumerate(feature_names):
            varied = np.tile(sample, (6, 1))
            deltas = np.linspace(-0.2, 0.2, 6) * (abs(sample[i]) + 1)
            varied[:, i] = sample[i] + deltas
            risks = self.model.predict_risk(varied)
            results[feature] = {"risk_range": float(risks.max() - risks.min())}
        return results

    def generate_report(self, X_test, y_test) -> str:
        auroc = self.evaluate_auroc(X_test, y_test)["auroc"]
        brier = self.evaluate_calibration(X_test, y_test)["brier_score"]
        return json.dumps({"auroc": auroc, "brier_score": brier}, indent=2)
