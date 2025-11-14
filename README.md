# Software Architectures in MLOps

This project demonstrates two architectural approaches for building predictive model services: a monolithic architecture and a microservices architecture.

## Project Structure

- **[monolith/](monolith/README.md)**: Single-service application with all models and prediction logic
- **[microservices/](microservices/README.md)**: Distributed system with service discovery, multiple model services, and a gateway
- **[modelling/](modelling/README.md)**: Jupyter notebooks and model training scripts

## Quick Start

### Monolith Architecture

For a simple, single-service deployment:

```bash
cd monolith
pip install -r requirements.txt
python main.py
```

Visit: http://localhost:8000

[→ Full Monolith Documentation](monolith/README.md)

### Microservices Architecture

For a distributed, scalable deployment with service discovery:

```bash
cd microservices
cp .env.example .env
docker-compose up --build
```

Visit: http://localhost:8000

[→ Full Microservices Documentation](microservices/README.md)

### Model Training

Train and develop new models:

```bash
cd modelling
pip install -r requirements.txt
jupyter notebook
```

[→ Full Modelling Documentation](modelling/README.md)

## Comparison

| Aspect | Monolith | Microservices |
|--------|----------|---------------|
| Deployment | Single container/process | Multiple containers |
| Scaling | Vertical scaling | Horizontal scaling |
| Service Discovery | N/A | Consul |
| Fault Isolation | Single point of failure | Isolated service failures |
| Development | Simpler | More complex |
| Latency | Lower | Higher (network calls) |

## Prerequisites

- Python 3.10+
- Docker and Docker Compose (for microservices)
- pip or conda for dependency management

## API Documentation

Once running, interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs