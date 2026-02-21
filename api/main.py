from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from model.predict import predict_diabetes

# Create FastAPI application
app = FastAPI(title="Diabetes Prediction API")

# Request schema
class PatientData(BaseModel):
    features: list[float] = Field(min_length=5, max_length=5)
    # [Pregnancies, Glucose, BloodPressure, BMI, Age]

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok"}

@app.post("/predict")
def predict(data: PatientData):
    """
    Prediction endpoint
    """
    try:
        prediction = predict_diabetes(data.features)
        return {
            "prediction": prediction,
            "label": "Diabetes" if prediction == 1 else "No Diabetes"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))