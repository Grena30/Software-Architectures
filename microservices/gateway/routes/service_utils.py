import httpx
import os
import random
from dotenv import load_dotenv


load_dotenv()
service_discovery_url = os.getenv("SERVICE_DISCOVERY_URL")


def get_healthy_services(service_name: str | None = None) -> list:
    if service_name is None:
        url = f"{service_discovery_url}/v1/health/services/"
    else:
        url = f"{service_discovery_url}/v1/health/service/{service_name}"

    resp = httpx.get(f"{url}")

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

def get_all_healthy_services() -> list:
    services = []
    catalog_url = f"{service_discovery_url}/v1/catalog/services"
    catalog_resp = httpx.get(catalog_url)
    if catalog_resp.status_code != 200:
        return []

    all_services = catalog_resp.json().keys()

    for s_name in all_services:
        url = f"{service_discovery_url}/v1/health/service/{s_name}?passing=true"
        health_resp = httpx.get(url)
        if health_resp.status_code == 200:
            for entry in health_resp.json():
                service = entry.get("Service", {})
                address = service.get("Address")
                port = service.get("Port")
                if address and port:
                    services.append(f"{address}:{port}")
    
    return services

def load_balancer(services: list[str]) -> str:
    selected_service = random.choice(services)
    return selected_service
