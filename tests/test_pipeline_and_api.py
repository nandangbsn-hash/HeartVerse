from pathlib import Path


def test_training_pipeline_smoke(tmp_path: Path):
    np = __import__("pytest").importorskip("numpy")
    __import__("pytest").importorskip("pandas")
    __import__("pytest").importorskip("sklearn")

    from datasets.prepare_datasets import prepare_all_datasets
    from ml.features import CardiovascularDataLoader
    from ml.train import CardiovascularRiskModel

    outputs = prepare_all_datasets(tmp_path)
    dataset = outputs["synthetic_cardiovascular"]

    loader = CardiovascularDataLoader()
    data = loader.prepare_data(str(dataset))

    model = CardiovascularRiskModel(model_type="gbdt")
    metrics = model.train(
        data["X_train"], data["y_train"], data["X_test"], data["y_test"], data["feature_names"]
    )
    assert metrics["train_rmse"] < 0.3
    assert np.isfinite(metrics["val_rmse"])


def test_api_assessment_endpoint():
    __import__("pytest").importorskip("fastapi")

    from fastapi.testclient import TestClient
    from backend.app import app

    client = TestClient(app)
    payload = {
        "age": 58,
        "sex": "M",
        "bp_systolic": 142,
        "bp_diastolic": 86,
        "cholesterol": 230,
        "resting_hr": 78,
        "bmi": 30,
        "ecg_regularity": 0.79,
        "heart_failure_flag": 0,
        "stress_score": 3,
        "fatigue_score": 3,
    }
    response = client.post("/api/assess-cardiovascular-health", json=payload)
    assert response.status_code == 200
    assert 0 <= response.json()["risk_score"] <= 1
