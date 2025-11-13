from fastapi import APIRouter
from schemas.predictive_model import InflationModel, GDPGrowthModel, UnemploymentModel
from prediction_services.gdp_growth_rate import get_prediction, model_name, get_model_paths


router = APIRouter(prefix="/api/predict", tags=["Predictions"])


@router.post("/")
def predict(model: GDPGrowthModel):
    prediction = get_prediction("gdp_growth_rate", model.model_dump())
    return {
        "message": "GDP growth prediction endpoint",
        "input": model.model_dump(),
        "model": model_name, 
        "prediction": prediction,
    }
    

