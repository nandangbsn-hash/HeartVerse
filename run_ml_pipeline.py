"""
Main training orchestration script.

This script:
1. Prepares datasets
2. Trains ML models
3. Evaluates and generates reports
4. Saves models for inference

Usage:
    python run_ml_pipeline.py
"""

import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from datasets.prepare_datasets import prepare_all_datasets
from ml.features import CardiovascularDataLoader
from ml.train import CardiovascularRiskModel, ModelEvaluator
from ml.evaluate import EvaluationVisualizer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run complete ML pipeline."""
    
    logger.info("="*70)
    logger.info("HEARTVERSE ML PIPELINE")
    logger.info("="*70)
    
    # Step 1: Prepare datasets
    logger.info("\n[STEP 1] Preparing datasets...")
    prepare_all_datasets()
    
    # Step 2: Check available datasets
    datasets_dir = Path(__file__).parent / 'datasets'
    available_datasets = list(datasets_dir.glob('*.csv'))
    
    if not available_datasets:
        logger.error("No datasets found! Cannot proceed.")
        return
    
    # Use synthetic dataset (guaranteed to exist)
    dataset_path = datasets_dir / 'synthetic_cardiovascular.csv'
    if not dataset_path.exists():
        logger.error(f"Dataset not found: {dataset_path}")
        return
    
    # Step 3: Load and prepare data
    logger.info("\n[STEP 2] Loading and preparing data...")
    loader = CardiovascularDataLoader()
    data = loader.prepare_data(str(dataset_path), test_size=0.2)
    
    logger.info(f"  - Training samples: {len(data['X_train'])}")
    logger.info(f"  - Test samples: {len(data['X_test'])}")
    logger.info(f"  - Features: {len(data['feature_names'])}")
    
    # Step 4: Train XGBoost model
    logger.info("\n[STEP 3] Training XGBoost risk model...")
    model = CardiovascularRiskModel(model_type='xgboost')
    
    # Split train into train/val for early stopping
    n_train = len(data['X_train'])
    n_val = max(n_train // 5, 100)  # At least 100 samples for validation
    
    train_metrics = model.train(
        X_train=data['X_train'][:-n_val],
        y_train=data['y_train'][:-n_val],
        X_val=data['X_train'][-n_val:],
        y_val=data['y_train'][-n_val:],
        feature_names=data['feature_names']
    )
    
    logger.info(f"  - Train RMSE: {train_metrics['train_rmse']:.4f}")
    logger.info(f"  - Train MAE: {train_metrics['train_mae']:.4f}")
    if 'val_rmse' in train_metrics:
        logger.info(f"  - Val RMSE: {train_metrics['val_rmse']:.4f}")
        logger.info(f"  - Val MAE: {train_metrics['val_mae']:.4f}")
    
    # Step 5: Evaluate model
    logger.info("\n[STEP 4] Evaluating model...")
    evaluator = ModelEvaluator(model)
    
    auroc_results = evaluator.evaluate_auroc(data['X_test'], data['y_test'])
    calib_results = evaluator.evaluate_calibration(data['X_test'], data['y_test'])
    
    logger.info(f"  - AUROC: {auroc_results['auroc']:.4f}")
    logger.info(f"  - Brier Score: {calib_results['brier_score']:.4f}")
    
    # Step 6: Sensitivity analysis
    logger.info("\n[STEP 5] Running sensitivity analysis...")
    baseline_sample = data['X_test'][0]
    sensitivity_results = evaluator.sensitivity_analysis(
        baseline_sample,
        data['feature_names']
    )
    
    logger.info("  - Top features by risk impact:")
    sorted_features = sorted(
        sensitivity_results.items(),
        key=lambda x: x[1]['risk_range'],
        reverse=True
    )
    for feature, results in sorted_features[:5]:
        logger.info(f"    • {feature}: Δrisk={results['risk_range']:.4f}")
    
    # Step 7: Create visualizations
    logger.info("\n[STEP 6] Creating evaluation visualizations...")
    visualizer = EvaluationVisualizer()
    
    visualizer.plot_auroc(auroc_results['fpr'], auroc_results['tpr'], 
                         auroc_results['auroc'])
    visualizer.plot_calibration(calib_results['prob_true'], calib_results['prob_pred'])
    visualizer.plot_sensitivity_analysis(sensitivity_results, data['feature_names'])
    
    y_pred_test = model.predict_risk(data['X_test'])
    visualizer.plot_risk_distribution(data['y_test'], y_pred_test)
    
    # Step 8: Generate comprehensive report
    logger.info("\n[STEP 7] Generating comprehensive report...")
    report = evaluator.generate_report(data['X_test'], data['y_test'])
    logger.info(report)
    
    # Step 9: Save model and metadata
    logger.info("\n[STEP 8] Saving model artifacts...")
    model.save()
    
    # Save metadata
    metadata = {
        'model_type': 'xgboost',
        'features': data['feature_names'],
        'train_samples': len(data['X_train']),
        'test_samples': len(data['X_test']),
        'auroc': auroc_results['auroc'],
        'brier_score': calib_results['brier_score'],
        'dataset': str(dataset_path)
    }
    
    import json
    with open(Path(__file__).parent / 'ml/models/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info("  - Model saved to ml/models/")
    logger.info("  - Metadata saved to ml/models/metadata.json")
    logger.info("  - Evaluations saved to ml/evaluation_results/")
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("ML PIPELINE COMPLETE!")
    logger.info("="*70)
    logger.info("\nNext steps:")
    logger.info("1. Review visualizations in ml/evaluation_results/")
    logger.info("2. Integrate model into FastAPI backend")
    logger.info("3. Test inference with sample patients")
    logger.info("4. Build 3D heart simulation")
    logger.info("5. Connect to React frontend")


if __name__ == "__main__":
    main()
