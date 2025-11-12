import httpx
import os
import random
from dotenv import load_dotenv


load_dotenv()
service_discovery_url = os.getenv("SERVICE_DISCOVERY_URL")


def get_healthy_services(service_name: str) -> list:
    resp = httpx.get(f"{service_discovery_url}/v1/health/service/{service_name}")

    if resp.status_code == 200:
        services = []
        for entry in resp.json():
            service = entry.get("Service", {})
            address = service.get("Address")
            port = service.get("Port")
            if address and port:
                services.append(f"{address}:{port}")
        return services
    return []


def load_balancer(services: list[str]) -> str:
    selected_service = random.choice(services)
    return selected_service
