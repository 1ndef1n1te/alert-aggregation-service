from fastapi import FastAPI
from .docs import descrition
from .api.v1.alert.alert import alert_router

app = FastAPI(
    title="oVirt Swagger",
    version="1.0.0",
    description=descrition,
    docs_url="/api/docs",
)


def create_app():
    app.include_router(alert_router)
    return app
