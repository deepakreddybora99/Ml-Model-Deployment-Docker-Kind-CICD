import os
import subprocess
import joblib
import numpy as np
import pandas as pd
import pytest
import subprocess
import sys

from model.predict import predict_diabetes, load_model

DATA_URL = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv"
MODEL_FILE = "model/diabetes_model.pkl"


# ---------------------------------------------------
# TRAINING TESTS
# ---------------------------------------------------


def test_training_script_runs_successfully():
    """
    Ensure train.py runs without errors
    """
    result = subprocess.run(
        [sys.executable, "model/train.py"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, result.stderr


def test_model_file_created_after_training():
    """
    Ensure model.pkl is created
    """
    assert os.path.exists(MODEL_FILE)


def test_model_can_be_loaded():
    """
    Ensure saved model can be loaded
    """
    model = joblib.load(MODEL_FILE)
    assert model is not None


# ---------------------------------------------------
# DATA VALIDATION TESTS
# ---------------------------------------------------

def test_dataset_schema():
    """
    Validate dataset columns
    """
    df = pd.read_csv(DATA_URL)

    expected_columns = [
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "BMI",
        "Age",
        "Outcome"
    ]

    for col in expected_columns:
        assert col in df.columns


# ---------------------------------------------------
# PREDICTION TESTS
# ---------------------------------------------------

def test_predict_diabetes_high_risk():
    """
    High-risk patient should return valid prediction
    """
    prediction = predict_diabetes([2, 180, 90, 35.0, 55])
    assert prediction in [0, 1]
    assert prediction == 1


def test_predict_diabetes_low_risk():
    """
    Low-risk patient should return valid prediction
    """
    prediction = predict_diabetes([0, 90, 70, 22.0, 25])
    assert prediction in [0, 1]
    assert prediction == 0


def test_predict_invalid_feature_length():
    """
    Invalid feature length should raise ValueError
    """
    with pytest.raises(ValueError):
        predict_diabetes([150, 80])  # too few features


def test_predict_invalid_feature_type():
    """
    Invalid feature type should raise TypeError
    """
    with pytest.raises(TypeError):
        predict_diabetes("invalid-input")


# ---------------------------------------------------
# SANITY CHECK: MODEL PREDICTION SHAPE
# ---------------------------------------------------

def test_model_prediction_shape():
    prediction = predict_diabetes([0, 120, 70, 25.0, 30])
    assert isinstance(prediction, int)