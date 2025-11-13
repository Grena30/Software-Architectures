from fastapi import APIRouter, HTTPException
from schemas.predictive_model import InflationModel, GDPGrowthModel, UnemploymentModel
from routes.service_utils import get_all_healthy_services, service_discovery_url
from pathlib import Path
import subprocess
import httpx
import os
import docker


router = APIRouter(prefix="/api/models", tags=["Admin"])
model_name = "gdp-growth-model"
client = docker.from_env()


@router.get("/available")
def list_available_models():
    services = get_all_healthy_services()

    if not services:
        raise HTTPException(status_code=503, detail="No model services available")

    models_by_service = {}
    for service in services:
        try:
            resp = httpx.get(
                f"http://{service}/api/status/available_models", timeout=5.0
            )
            if resp.status_code == 200:
                models_by_service[service] = resp.json()["models"]
        except Exception as e:
            print(f"Error fetching models from {service}: {e}")

    return {"models_by_service": models_by_service, "services": services}


@router.post("/launch/{model_name}")
def launch_model_instance(model_name: str):
    try:
        next_number = 1
        container_name = f"microservices-gdp-growth-model-{next_number}"
        existing = client.containers.list(all=True, filters={"name": container_name})
        # Check if container already exists
        while True:
            container_name = f"microservices-gdp-growth-model-{next_number}"
            # Check if a container with this exact name exists
            exists = client.containers.list(all=True, filters={"name": container_name})
            if not exists:
                break
            next_number += 1
            # return {
            #     "status": "failed",
            #     "message": f"Container {container_name} already exists.",
            # }

        # Launch new container
        container = client.containers.run(
            image="microservices-gdp-growth-model",
            name=container_name,
            detach=True,
            environment={
                "GDP_MODEL_NAME": model_name,
                "SERVICE_DISCOVERY_URL": service_discovery_url,
            },
            labels={"model": model_name}
        )
        
        network = client.networks.get("microservices_compute-network")
        network.connect(container)

        return {
            "status": "success",
            "message": f"Launched new instance for model: {model_name}",
            "container_id": container.id,
            "container_name": container.name,
        }

    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=f"Docker error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/instances/{model_name}")
def get_model_instances(model_name: str):
    try:
        containers = client.containers.list(
            all=True, filters={"label": f"model={model_name}"}
        )
        instances = [
            {
                "id": c.id,
                "name": c.name,
                "status": c.status,
                "image": c.image.tags,
            }
            for c in containers
        ]
        return {"model": model_name, "instances": instances}

    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=f"Docker error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/instances/{container_id}")
def delete_model_instance(container_id: str):
    try:
        container = client.containers.get(container_id)
        container.stop(timeout=10)
        return {
            "status": "success",
            "message": f"Shutdown container: {container_id}",
        }

    except docker.errors.NotFound:
        raise HTTPException(
            status_code=404, detail=f"Container {container_id} not found"
        )
    except docker.errors.DockerException as e:
        raise HTTPException(status_code=500, detail=f"Docker error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
