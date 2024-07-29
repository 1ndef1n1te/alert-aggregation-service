from fastapi import FastAPI
from .docs import descrition
from .api.v1.alert.alert import alert_router
from .api.app_status import status_router
from .external.init_data import init_data
import os

app = FastAPI(
    title="oVirt Swagger",
    version="1.0.0",
    description=descrition,
    docs_url="/api/docs",
)


def create_app():
    app.include_router(alert_router)
    app.include_router(status_router)
    app.add_event_handler("startup", lambda: os.makedirs(f"./data", exist_ok=True))
    app.add_event_handler("startup", init_data)
    return app
