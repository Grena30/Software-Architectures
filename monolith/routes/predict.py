from fastapi import APIRouter
from models.predictive_model import InflationModel, GDPGrowthModel, UnemploymentModel
from preprocessing.predict import get_prediction


router = APIRouter(prefix="/api/predict", tags=["cluster"])


@router.post("/gdp_growth")
def predict_(model: GDPGrowthModel):
    prediction = get_prediction("gdp_growth_rate", model.model_dump())
    return {
        "message": "GDP growth prediction endpoint",
        "input": model.model_dump(),
        "prediction": prediction,
    }


@router.post("/inflation")
def predict_inflation(model: InflationModel):
    prediction = get_prediction("inflation_rate", model.model_dump())
    return {
        "message": "Inflation prediction endpoint",
        "input": model.model_dump(),
        "prediction": prediction,
    }


@router.post("/unemployment")
def predict_unemployment(model: UnemploymentModel):
    prediction = get_prediction("unemployment_rate", model.model_dump())
    return {
        "message": "Unemployment prediction endpoint",
        "input": model.model_dump(),
        "prediction": prediction,
    }
