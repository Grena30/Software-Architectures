import pandas as pd
from preprocessing.utils import get_models


loaded_models = get_models()


def get_prediction(prediction_type: str, data: dict) -> list:

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
