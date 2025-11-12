from fastapi import APIRouter
from schemas.predictive_model import InflationModel, GDPGrowthModel, UnemploymentModel
from routes.service_utils import get_healthy_services, load_balancer
import httpx


router = APIRouter(prefix="/api/predict", tags=["Prediction"])
model_name = "gdp-growth-model"


@router.post("/gdp_growth_rate")
def predict_gdp_growth(model: GDPGrowthModel):
    services = get_healthy_services(service_name=model_name)
    if not services:
        return {"error": "No healthy services available for prediction."}

    # Round robin selection of service
    service = load_balancer(services)

    resp = httpx.post(
        f"http://{service}/api/predict/gdp_growth_rate",
        json=model.model_dump(),
        timeout=10.0,
    ).json()

    prediction = resp["prediction"]
    return {
        "message": "GDP growth prediction endpoint",
        "input": model.model_dump(),
        "prediction": prediction,
    }


@router.get("/services")
def get_model_services():
    services = get_healthy_services(service_name=model_name)

    return {"Services:": services}
