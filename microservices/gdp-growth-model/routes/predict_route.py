from fastapi import APIRouter
from schemas.predictive_model import InflationModel, GDPGrowthModel, UnemploymentModel
from prediction_services.gdp_growth_rate import get_prediction


router = APIRouter(prefix="/api/predict", tags=["cluster"])


@router.post("/gdp_growth_rate")
def predict_(model: GDPGrowthModel):
    prediction = get_prediction("gdp_growth_rate", model.model_dump())
    return {
        "message": "GDP growth prediction endpoint",
        "input": model.model_dump(),
        "prediction": prediction,
    }
