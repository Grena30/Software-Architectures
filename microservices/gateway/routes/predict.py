from fastapi import APIRouter
from models.predictive_model import InflationModel, GDPGrowthModel, UnemploymentModel


router = APIRouter(prefix="/api/predict", tags=["cluster"])


@router.post("/gdp_growth_rate")
def predict_gdp_growth(model: GDPGrowthModel):
    prediction = []
    # prediction = get_prediction("gdp_growth_rate", model.model_dump())
    return {
        "message": "GDP growth prediction endpoint",
        "input": model.model_dump(),
        "prediction": prediction,
    }
