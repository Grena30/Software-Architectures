import socket
import os
from consul import Consul
from dotenv import load_dotenv


load_dotenv()

SERVICE_PORT = 5000
SERVICE_DISCOVERY_PORT = 8500
HOST = "service-discovery"
GDP_MODEL_NAME = os.getenv("GDP_MODEL_NAME", "LinearRegression")

def register_gdp_model():
    consul = Consul(host=HOST, port=SERVICE_DISCOVERY_PORT)
    ip_address = socket.gethostbyname(socket.gethostname())
    service_id = f"gdp-growth-model-{GDP_MODEL_NAME}-{ip_address}"

    consul.agent.service.register(
        name="gdp-growth-model",
        service_id=service_id,
        address=ip_address,
        port=SERVICE_PORT,
        tags=["model", "gdp", f"model:{GDP_MODEL_NAME}"],
        check={"http": f"http://{ip_address}:{SERVICE_PORT}/health", "interval": "10s"},
    )
    print(f"Registered {service_id} with model {GDP_MODEL_NAME}")


def deregister_gdp_model():
    consul = Consul(host=HOST, port=SERVICE_DISCOVERY_PORT)
    ip_address = socket.gethostbyname(socket.gethostname())
    service_id = f"gdp-growth-model-{GDP_MODEL_NAME}-{ip_address}"
    consul.agent.service.deregister(service_id)
    print(f"Deregistered {service_id} from Consul")
