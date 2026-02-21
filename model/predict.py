import joblib
import pandas as pd
import numpy as np
import os

# Path to trained model
MODEL_PATH = "model/diabetes_model.pkl"

# Expected feature order (MUST match training)
FEATURE_NAMES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "BMI",
    "Age"
]


def load_model():
    """
    Load trained ML model from disk
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Model file not found. Ensure diabetes_model.pkl exists."
        )

    return joblib.load(MODEL_PATH)


def predict_diabetes(features):
    """
    Predict diabetes outcome

    Parameters:
    features (list or array): 
        [Pregnancies, Glucose, BloodPressure, BMI, Age]

    Returns:
    int: 0 (No Diabetes) or 1 (Diabetes)
    """

    # ✅ 1. Type check FIRST
    if not isinstance(features, (list, tuple, np.ndarray)):
        raise TypeError("Features must be a list, tuple, or numpy array")

    # ✅ 2. Length check SECOND
    if len(features) != len(FEATURE_NAMES):
        raise ValueError("Invalid number of features")

    model = load_model()

    features_df = pd.DataFrame([features], columns=FEATURE_NAMES)
    prediction = model.predict(features_df)

    return int(prediction[0])

print("Prediction pipeline Run Successfully")