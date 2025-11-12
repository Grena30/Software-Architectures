import pandas as pd
import joblib
import os


models_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "predictive_models"
)


def get_model_paths() -> dict:
    models = {}
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


def get_models(model_name: str = "") -> dict:

    models = get_model_paths()
    if not models:
        return {}

    loaded_models = {}

    if not model_name or model_name not in models.keys():
        model_name = "LinearRegression"
        print("Model name not found, switching to default")

    for target in models.keys():
        model = model_name + ".pkl"
        path = os.path.join(models_path, target, model)
        loaded_models[target] = joblib.load(path)

    return loaded_models


def get_prediction(prediction_type: str, data: dict) -> list:
    loaded_models = get_models()
    prediction = []

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
