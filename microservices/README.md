# Microservices Architecture

A distributed system with multiple services connected via service discovery, providing scalable model serving capabilities.

## Quick Start

1. Navigate to the microservices directory:
```bash
cd microservices
```

2. Set up environment:
```bash
cp .env.example .env
```

3. Update `.env` with your configuration:
```env
SERVICE_DISCOVERY_URL=http://service-discovery:8500
GDP_MODEL_NAME=LinearRegression
```

4. Ensure model files are in place in `gdp-growth-model/predictive_models/`:
```
gdp-growth-model/predictive_models/
└── gdp_growth_rate/
    ├── LinearRegression.pkl
    └── (other models)
```

5. Start all services:
```bash
docker-compose up --build
```

The gateway API will be available at `http://localhost:8000`

## Services Overview

### Service Discovery (Consul)

- **Port**: 8500
- **UI**: http://localhost:8500/ui
- **Purpose**: Service registration and health checking
- **Features**: Automatic service discovery and health monitoring

### Gateway

- **Port**: 8000
- **Purpose**: API gateway and load balancer
- **Features**:
  - Request routing to healthy services
  - Service discovery integration
  - Container management
  - Random load balancing

### GDP Growth Model Service

- **Port**: 5000 (internal)
- **Replicas**: 2 (configurable)
- **Purpose**: Serves GDP growth predictions
- **Features**: Auto-registers with Consul on startup

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                   Docker Compose Network            │
│                  (compute-network)                  │
│                                                     │
│  ┌──────────────┐      ┌──────────────────────┐     │
│  │  Consul      │      │      Gateway         │     │
│  │  :8500       │◄─────┤      :8000           │     │
│  └──────────────┘      │  - Load balancer     │     │
│       ▲                │  - Service discovery │     │
│       │ (register)     │  - Container mgmt    │     │
│       │                └──────────────────────┘     │
│       │                        │                    │
│       │                        │ (route requests)   │
│       │                        ▼                    │
│       │             ┌──────────────────────┐        │
│       │             │ Model Service 1      │        │
│       └─────────────┤ :5000                │        │
│       │             │ - GDP Growth Model   │        │
│       │             └──────────────────────┘        │
│       │             ┌──────────────────────┐        │
│       │             │ Model Service 2      │        │
│       └─────────────┤ :5000                │        │
│                     │ - GDP Growth Model   │        │
│                     └──────────────────────┘        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## API Endpoints

### GET /api/models/available

List all available models across all services.

**Request:**
```bash
curl http://localhost:8000/api/models/available
```

**Response:**
```json
{
  "models_by_service": {
    "gdp-growth-model-1:5000": ["LinearRegression", "RandomForest"]
  },
  "services": ["gdp-growth-model-1:5000"]
}
```

### POST /api/predict/gdp_growth_rate

Predict GDP growth rate using load-balanced service instance.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/predict/gdp_growth_rate" \
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
  "input": {...},
  "model": "LinearRegression",
  "prediction": [2.45]
}
```

### GET /api/predict/services

Get all healthy services.

**Request:**
```bash
curl http://localhost:8000/api/predict/services
```

**Response:**
```json
{
  "Services:": [
    "gdp-growth-model-1:5000",
    "gdp-growth-model-2:5000"
  ]
}
```

### POST /api/models/launch/{model_name}

Launch a new instance of a model service.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/models/launch/LinearRegression"
```

**Response:**
```json
{
  "status": "success",
  "message": "Launched new instance for model: LinearRegression",
  "container_id": "abc123...",
  "container_name": "microservices-gdp-growth-model-3"
}
```

### GET /api/models/instances/{model_name}

Get all instances of a specific model.

**Request:**
```bash
curl http://localhost:8000/api/models/instances/LinearRegression
```

**Response:**
```json
{
  "model": "LinearRegression",
  "instances": [
    {
      "id": "abc123...",
      "name": "microservices-gdp-growth-model-1",
      "status": "running",
      "image": ["microservices-gdp-growth-model:latest"]
    }
  ]
}
```

### DELETE /api/models/instances/{container_id}

Stop and remove a model instance.

**Request:**
```bash
curl -X DELETE "http://localhost:8000/api/models/instances/abc123"
```

**Response:**
```json
{
  "status": "success",
  "message": "Shutdown container: abc123"
}
```

## Project Structure

```
microservices/
├── compose.yaml                    # Docker Compose configuration
├── .env                            # Environment variables
├── .env.example                    # Environment template
├── .dockerignore                   # Docker build ignore patterns
├── gateway/
│   ├── main.py                     # Gateway FastAPI app
│   ├── Dockerfile                  # Gateway container image
│   ├── requirements.txt            # Dependencies
│   ├── routes/
│   │   ├── predict_route.py       # Prediction routing
│   │   ├── model_management.py    # Model lifecycle management
│   │   └── service_utils.py       # Service discovery utilities
│   └── schemas/
│       ├── predictive_model.py    # Request/response models
│       └── services.py             # Service models
├── gdp-growth-model/
│   ├── main.py                     # Model service app
│   ├── Dockerfile                  # Container image
│   ├── requirements.txt            # Dependencies
│   ├── service_registry.py         # Consul registration
│   ├── routes/
│   │   ├── predict_route.py       # Prediction endpoint
│   │   └── model_info.py          # Model info endpoints
│   ├── schemas/
│   │   └── predictive_model.py    # Data models
│   ├── prediction_services/
│   │   └── gdp_growth_rate.py     # Prediction logic
│   └── predictive_models/
│       └── gdp_growth_rate/       # Model files
├── service-discovery/
│   └── Dockerfile                  # Consul container image
```

## Scaling Services

### Scale GDP Growth Model to 5 instances

```bash
docker-compose up -d --scale gdp-growth-model=5
```

### View running services

```bash
docker-compose ps
```

### Stop all services

```bash
docker-compose down
```

## Monitoring and Debugging

### View Consul UI

http://localhost:8500/ui

### View service logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f gdp-growth-model

# Follow new logs only
docker-compose logs -f --tail=50
```

### Check service health via Consul API

```bash
curl http://localhost:8500/v1/health/service/gdp-growth-model
```

### Health check endpoint

Each model service exposes a health endpoint:

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "ok",
  "model": "LinearRegression"
}
```

## Configuration

### Environment Variables (.env)

```env
SERVICE_DISCOVERY_URL=http://service-discovery:8500
GDP_MODEL_NAME=LinearRegression
```

### Docker Compose Configuration (compose.yaml)

Edit to modify:
- Number of replicas: `deploy.replicas`
- Port mappings: `ports`
- Environment variables: `env_file`, `environment`
- Network settings: `networks`

## Troubleshooting

### Service not registering with Consul

1. Check Consul is running:
```bash
docker-compose ps service-discovery
```

2. Verify `SERVICE_DISCOVERY_URL` in `.env`

3. Check logs:
```bash
docker-compose logs service-discovery
```

### Model service not responding

1. Verify container is running:
```bash
docker-compose ps gdp-growth-model
```

2. Check logs:
```bash
docker-compose logs gdp-growth-model
```

3. Test health endpoint:
```bash
curl http://localhost:5000/health
```

### Container can't reach Consul

1. Ensure containers are on the same network: `compute-network`
2. Use `service-discovery` as hostname (not localhost or IP addresses)
3. Check network connectivity:
```bash
docker-compose exec gdp-growth-model ping service-discovery
```

### Load balancing not working

1. Check Consul UI for healthy service instances
2. Verify health check is passing
3. Check gateway logs for routing decisions

## Advantages

- Horizontal scaling of individual services
- Service isolation and fault tolerance
- Independent deployment and updates
- Easy to add new services
- Better resource utilization

## Disadvantages

- Higher operational complexity
- Network latency between services
- Distributed debugging is harder
- Requires Docker and orchestration knowledge
- More moving parts to monitor

## Documentation

Interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs

---

[← Back to main README](../README.md)