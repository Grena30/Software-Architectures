# Monolith Architecture

A single-service application that handles all predictive model requests in one unified service.

## Quick Start

1. Navigate to the monolith directory:
```bash
cd monolith
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure model files are in place:
```
predictive_models/
├── gdp_growth_rate/
│   ├── LinearRegression.pkl
│   └── (other models)
├── inflation_rate/
│   ├── LinearRegression.pkl
│   └── (other models)
└── unemployment_rate/
    ├── LinearRegression.pkl
    └── (other models)
```

4. Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Features

- **GDP Growth Prediction**: Predict GDP growth rates based on economic indicators
- **Inflation Prediction**: Forecast inflation rates
- **Unemployment Prediction**: Estimate unemployment rates
- **Single deployment**: No service discovery or orchestration needed

## API Endpoints

### POST /api/predict/gdp_growth

Predict GDP growth rate.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/predict/gdp_growth" \
  -H "Content-Type: application/json" \
  -d '{
    "gdp_per_capita": 50000,
    "unemployment_rate": 5.2,
    "gdp_growth_rate_lag": 2.1,
    "gdp_growth_rate_ma": 2.3
  }'
```

**Response:**
```json
{
  "message": "GDP growth prediction endpoint",
  "input": {
    "gdp_per_capita": 50000,
    "unemployment_rate": 5.2,
    "gdp_growth_rate_lag": 2.1,
    "gdp_growth_rate_ma": 2.3
  },
  "prediction": [2.45]
}
```

### POST /api/predict/inflation

Predict inflation rate.

**Request Body:**
```json
{
  "inflation_rate_lag": 2.1,
  "inflation_rate_monthly": 0.2,
  "unemployment_rate": 5.2
}
```

### POST /api/predict/unemployment

Predict unemployment rate.

**Request Body:**
```json
{
  "unemployment_rate_lag": 5.2,
  "gdp_growth_rate_ma": 2.3
}
```

## Project Structure

```
monolith/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── routes/
│   └── predict.py            # Prediction endpoints
├── models/
│   └── predictive_model.py   # Pydantic data models
├── preprocessing/
│   ├── predict.py            # Prediction logic
│   └── utils.py              # Model loading utilities
└── predictive_models/
    ├── gdp_growth_rate/      # GDP growth models
    ├── inflation_rate/       # Inflation models
    └── unemployment_rate/    # Unemployment models
```

## Architecture

The monolith application follows a simple layered architecture:

1. **API Layer** ([`routes/predict.py`](routes/predict.py)): Handles HTTP requests
2. **Data Models** ([`models/predictive_model.py`](models/predictive_model.py)): Validates request/response data
3. **Business Logic** ([`preprocessing/predict.py`](preprocessing/predict.py)): Executes predictions
4. **Data Access** ([`preprocessing/utils.py`](preprocessing/utils.py)): Loads pre-trained models

## Model Management

Models are loaded at startup and cached in memory.

### Using a Different Model

1. Place the model file in the appropriate `predictive_models/{model_type}/` directory
2. Model filename format: `{ModelName}.pkl`
3. Update [`preprocessing/utils.py`](preprocessing/utils.py) to reference the new model

### Adding a New Prediction Type

1. Add a new Pydantic model in [`models/predictive_model.py`](models/predictive_model.py)
2. Create a new route in [`routes/predict.py`](routes/predict.py)
3. Place model files in a new subdirectory under `predictive_models/`

## Documentation

Interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs

## Advantages

- Simple deployment and development
- Lower latency (no network calls between services)
- Easier debugging and monitoring
- Minimal operational overhead

## Disadvantages

- Difficult to scale individual components
- Single point of failure
- Requires redeployment of entire application for any change
- Resource-intensive if models are rarely used

---

[← Back to main README](../README.md)