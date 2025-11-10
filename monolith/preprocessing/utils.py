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

    for target, model in models.items():
        model = model_name + ".pkl"
        path = os.path.join(models_path, target, model)
        loaded_models[target] = joblib.load(path)

    return loaded_models
