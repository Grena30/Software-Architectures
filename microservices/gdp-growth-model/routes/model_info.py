from fastapi import APIRouter
from schemas.predictive_model import InflationModel, GDPGrowthModel, UnemploymentModel
from prediction_services.gdp_growth_rate import get_prediction, get_model_paths
import os


router = APIRouter(prefix="/api/status", tags=["Status"])
GDP_MODEL_NAME = os.getenv("GDP_MODEL_NAME", "LinearRegression")


@router.get("/model_info")
def model_info():
    return {"model_name": GDP_MODEL_NAME, "service_name": "gdp-growth-model"}


@router.get("/available_models")
def available_models():
    paths = get_model_paths()
    
    return {
        "message": "GDP growth models",
        "models": paths['gdp_growth_rate']   
    }
