import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib


DATA_URL = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv"
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "diabetes_model.pkl")


def train_model():
    """
    Train RandomForest model and save it to disk
    """

    # Load dataset
    df = pd.read_csv(DATA_URL)

    # Prepare data
    X = df[["Pregnancies", "Glucose", "BloodPressure", "BMI", "Age"]]
    y = df["Outcome"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Ensure model directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Save model
    joblib.dump(model, MODEL_PATH)

    print("Model trained and saved at:", MODEL_PATH)


def main():
    train_model()


if __name__ == "__main__":
    main()