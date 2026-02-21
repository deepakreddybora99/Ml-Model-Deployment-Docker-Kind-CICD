from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# -----------------------------------------
# HEALTH CHECK TESTS
# -----------------------------------------

def test_health_endpoint():
    """
    Health endpoint should return status ok
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# -----------------------------------------
# PREDICTION ENDPOINT TESTS
# -----------------------------------------

def test_predict_valid_high_risk_input():
    """
    High-risk patient should return valid prediction
    """
    payload = {
        "features": [2, 180, 90, 35.0, 55]
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] in [0, 1]
    assert response.json()["label"] in ["Diabetes", "No Diabetes"]


def test_predict_valid_low_risk_input():
    """
    Low-risk patient should return valid prediction
    """
    payload = {
        "features": [0, 90, 70, 22.0, 25]
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert response.json()["prediction"] == 0
    assert response.json()["label"] == "No Diabetes"


# -----------------------------------------
# INPUT VALIDATION TESTS
# -----------------------------------------

def test_predict_invalid_feature_length():
    """
    Invalid feature length should return 422
    """
    payload = {
        "features": [120, 70]  # too few features
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_missing_features_field():
    """
    Missing features field should return 422
    """
    payload = {}

    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_invalid_feature_type():
    """
    Invalid feature type should return 422
    """
    payload = {
        "features": ["invalid", "data", "types", "here", "x"]
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 422


# -----------------------------------------
# ERROR HANDLING TEST
# -----------------------------------------

def test_predict_internal_error_handling(monkeypatch):
    """
    Force internal error and verify graceful handling
    """

    def mock_predict(_):
        raise Exception("Model failure")

    monkeypatch.setattr("api.main.predict_diabetes", mock_predict)

    payload = {
        "features": [1, 140, 85, 30.0, 45]
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 400
    assert "Model failure" in response.json()["detail"]