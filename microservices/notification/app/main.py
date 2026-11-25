"""Notification microservice - entry point.

Run:  python -m app.main                                   (port 8084 by default)
  or: uvicorn app.main:app --reload --port 8084

Second instance (Eureka load-balancing demo) - PORT must match the listening port:
  PowerShell: $env:PORT=8094; python -m app.main
  bash:       PORT=8094 python -m app.main

The service registers itself in Eureka as NOTIFICATION at startup and
deregisters on shutdown (Ctrl+C). Set EUREKA_ENABLED=false to disable it.
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.eureka import create_eureka_client, eureka_enabled
from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Register in Eureka at startup, deregister at shutdown."""
    client = None
    if eureka_enabled():
        client = create_eureka_client(PORT)
        try:
            await client.start()  # register + heartbeat every 30 s
            print(f"Registered in Eureka as NOTIFICATION (localhost:{PORT})")
        except Exception as e:  # Eureka unreachable: the service still starts
            print(f"Eureka registration failed: {e}")

    yield  # ---- the application is running ----

    if client is not None:
        try:
            await client.stop()  # deregister (cancel) from Eureka
            print("Deregistered from Eureka")
        except Exception:
            pass


app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    # Same URLs as the other microservices of the project
    docs_url="/swagger-ui",       # Swagger UI
    openapi_url="/v3/api-docs",   # OpenAPI JSON
    redoc_url="/redoc",           # alternative documentation
    lifespan=lifespan,            # Eureka registration / deregistration
)

app.include_router(notification.router)

# TODO (students): if you add other routers, include them here.


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)
