# app/eureka.py – enregistre le service notification dans Eureka sous le nom NOTIFICATION
import os
from py_eureka_client.eureka_client import EurekaClient

APP_NAME = "NOTIFICATION"


def get_port() -> int:
    return int(os.getenv("PORT", "8084"))


def eureka_enabled() -> bool:
    return os.getenv("EUREKA_ENABLED", "true").lower() != "false"


def create_eureka_client(port: int) -> EurekaClient:
    host = os.getenv("EUREKA_INSTANCE_HOST", "localhost")
    ip = os.getenv("EUREKA_INSTANCE_IP", "127.0.0.1")
    base_url = f"http://{host}:{port}"
    return EurekaClient(
        eureka_server=os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka"),
        app_name=APP_NAME,
        instance_host=host,
        instance_ip=ip,
        instance_port=port,
        home_page_url=f"{base_url}/swagger-ui",
        status_page_url=f"{base_url}/api/notifications/hello",
        health_check_url=f"{base_url}/api/notifications/hello",
    )
