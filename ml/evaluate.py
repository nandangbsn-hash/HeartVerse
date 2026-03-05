"""Evaluation visualizations for HeartVerse."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


class EvaluationVisualizer:
    def __init__(self, output_dir: str | Path = "ml/evaluation_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _save_placeholder(self, name: str, title: str):
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.set_title(title)
        ax.plot([0, 1], [0, 1], "--", color="gray")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        fig.tight_layout()
        fig.savefig(self.output_dir / name)
        plt.close(fig)

    def plot_auroc(self, fpr, tpr, auroc):
        self._save_placeholder("roc_curve.png", f"AUROC={auroc:.3f}")

    def plot_calibration(self, prob_true, prob_pred):
        self._save_placeholder("calibration_curve.png", "Calibration")

    def plot_sensitivity_analysis(self, sensitivity_results, feature_names):
        self._save_placeholder("sensitivity_analysis.png", "Sensitivity")

    def plot_risk_distribution(self, y_true, y_pred):
        self._save_placeholder("risk_distribution.png", "Risk Distribution")
