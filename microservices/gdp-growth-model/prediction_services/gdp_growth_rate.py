import pandas as pd
import joblib
import os
from dotenv import load_dotenv


load_dotenv()
GDP_GROWTH_MODEL = os.getenv("GDP_MODEL_NAME", "LinearRegression")


models_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "predictive_models"
)


def get_model_paths() -> dict:
    models = {}

    if not os.path.exists(models_path):
        print(f"Models path does not exist: {models_path}")
        return {}

    subdirs = [
        model
        for model in os.listdir(models_path)
        if os.path.isdir(os.path.join(models_path, model))
    ]

    for dir in subdirs:
        dir_path = os.path.join(models_path, dir)

        models[dir] = [
            file
            for file in os.listdir(dir_path)
            if file.endswith((".pkl", ".pt", ".h5", ".joblib"))
        ]

    if not models:
        print("No models available")
        return {}

    return models


def get_models(model_name: str | None = None) -> tuple[dict, str]:

    models = get_model_paths()
    if not models:
        return {}, ""
    
    if not model_name or (model_name + ".pkl") not in models["gdp_growth_rate"]:
        model_name = "LinearRegression"
        print("Model name not found, switching to default")
    
    model = model_name + ".pkl"
    loaded_models = {}

    for target in models.keys():
        path = os.path.join(models_path, target, model)
        if os.path.exists(path):
            loaded_models[target] = joblib.load(path)
        else:
            print(f"Warning: Model file not found at {path}")

    return loaded_models, model_name


loaded_models, model_name = get_models(GDP_GROWTH_MODEL)


def get_prediction(prediction_type: str, data: dict) -> list:
    global loaded_models

    prediction = []

    if loaded_models is None:
        print("No model found model registry")
        return prediction

    if prediction_type not in loaded_models.keys():
        print("No model found for this type of prediction")
        return prediction

    if data is None or None in data.values():
        print("Invalid input data")
        return prediction

    try:
        X_input = pd.DataFrame.from_dict([data])  # type: ignore
        prediction = loaded_models[prediction_type].predict(X_input).tolist()
    except Exception as e:
        print(f"Error during prediction: {e}")

    return prediction


if __name__ == "__main__":
    print(
        get_prediction(
            "gdp_growth_rate",
            {
                "gdp_per_capita": 0,
                "unemployment_rate": 0,
                "gdp_growth_rate_lag": 0,
                "gdp_growth_rate_ma": 0,
            },
        )
    )
