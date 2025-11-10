import pandas as pd
from preprocessing.utils import get_models


loaded_models = get_models()


def get_prediction(type: str, data: dict) -> list:
    if type not in loaded_models.keys():
        print("No model found for this type of prediction")
        return []

    X_input = pd.DataFrame.from_dict([data])  # type: ignore
    print(X_input)
    prediction = loaded_models[type].predict(X_input)
    return prediction


if __name__ == "__main__":
    print(
        get_prediction(
            "gdp_growth_rate",
            {
                "gdp_per_capita": 40000,
                "unemployment_rate": 5.3,
                "gdp_growth_rate_lag": 3.9,
                "gdp_growth_rate_ma": 2.5,
            },
        )
    )
