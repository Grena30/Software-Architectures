from fastapi import APIRouter, HTTPException
from schemas.predictive_model import InflationModel, GDPGrowthModel, UnemploymentModel
from routes.service_utils import get_all_healthy_services, service_discovery_url
from pathlib import Path
import subprocess
import httpx
import os


router = APIRouter(prefix="/api/models", tags=["Admin"])
model_name = "gdp-growth-model"



@router.get("/available")
def list_available_models():
    services = get_all_healthy_services()

    if not services:
        raise HTTPException(status_code=503, detail="No model services available")

    models_by_service = {}
    for service in services:
        try:
            resp = httpx.get(f"http://{service}/available-models", timeout=5.0)
            if resp.status_code == 200:
                models_by_service[service] = resp.json()["available_models"]
        except Exception as e:
            print(f"Error fetching models from {service}: {e}")

    return {"models_by_service": models_by_service}


@router.post("/launch/{model_name}")
def launch_model_instance(model_name: str):
    try:
        # Create .env.model file for the new instance
        env_content = f"""GDP_MODEL_NAME={model_name}
                    SERVICE_DISCOVERY_URL={service_discovery_url}"""

        env_file_path = Path(f".env.{model_name}")
        with open(env_file_path, "w") as f:
            f.write(env_content)

        # Use docker-compose to start new service
        service_name = f"gdp-growth-model-{model_name}"

        result = subprocess.run(
            [
                "docker",
                "compose",
                "run",
                "-d",
                "--name",
                service_name,
                "--env-file",
                str(env_file_path),
                "gdp-growth-model",
            ],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        )

        if result.returncode == 0:
            return {
                "status": "success",
                "message": f"Launched new instance for model: {model_name}",
                "service_name": service_name,
                "container_id": result.stdout.strip(),
            }
        else:
            return {
                "status": "failed",
                "error": result.stderr,
                "message": f"Failed to launch model: {model_name}",
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/instances/{model_name}")
def get_model_instances(model_name: str):
    try:
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--filter",
                f"label=model={model_name}",
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            import json

            containers = json.loads(result.stdout) if result.stdout else []
            return {"model": model_name, "instances": containers}
        else:
            raise HTTPException(status_code=500, detail=result.stderr)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/instances/{container_id}")
def delete_model_instance(container_id: str):
    """Delete a specific model instance"""
    try:
        result = subprocess.run(
            ["docker", "rm", "-f", container_id], capture_output=True, text=True
        )

        if result.returncode == 0:
            return {
                "status": "success",
                "message": f"Deleted container: {container_id}",
            }
        else:
            return {"status": "failed", "error": result.stderr}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
