from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import os

api = FastAPI(
    title="Car Price Prediction API",
    version="1.0.0"
)

model = None

@api.on_event("startup")
async def load_model():
    global model
    model_path = os.getenv("MODEL_PATH", "/app/models/model.pkl")
    try:
        model = joblib.load(model_path)
        print(f"✓ Model loaded from {model_path}")
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        raise

class CarFeatures(BaseModel):
    Manufacturer: str
    Model: str
    Fuel_type: str = Field(alias="Fuel type")
    Engine_size: float = Field(alias="Engine size")
    Year_of_manufacture: int = Field(alias="Year of manufacture")
    Mileage: float

@api.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@api.post("/predict")
async def predict(features: CarFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        CURRENT_YEAR = 2025
        age = max(CURRENT_YEAR - features.Year_of_manufacture, 0)
        mileage_per_year = features.Mileage / max(age, 1)
        vintage = int(age >= 20)
        
        row = {
            "Manufacturer": features.Manufacturer,
            "Model": features.Model,
            "Fuel type": features.Fuel_type,
            "Engine size": features.Engine_size,
            "Year of manufacture": features.Year_of_manufacture,
            "Mileage": features.Mileage,
            "age": age,
            "mileage_per_year": mileage_per_year,
            "vintage": vintage,
        }
        df = pd.DataFrame([row])
        prediction = model.predict(df)[0]
        
        return {"predicted_price_gbp": float(prediction)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
