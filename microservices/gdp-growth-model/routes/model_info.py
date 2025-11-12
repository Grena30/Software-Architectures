from fastapi import APIRouter
from schemas.predictive_model import InflationModel, GDPGrowthModel, UnemploymentModel
from prediction_services.gdp_growth_rate import get_prediction, get_model_paths
import os


router = APIRouter(prefix="/api/status", tags=["Status"])
GDP_MODEL_NAME = os.getenv("GDP_MODEL_NAME", "LinearRegression")


@router.get("/model-info")
def model_info():
    return {"model_name": GDP_MODEL_NAME, "service_name": "gdp-growth-model"}


@router.get("/available-models")
def available_models():
    models = get_model_paths()
    return {"available_models": list(models.keys())}
