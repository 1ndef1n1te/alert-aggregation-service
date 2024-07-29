from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
import aiohttp
from ..settings import settings
from loguru import logger

status_router = APIRouter(prefix="/api", tags=["status"])


@status_router.get("/ping")
def ping():
    return "OK"


@status_router.get("/test-alert")
async def check_readiness():
    alert_message = "Test alert"
    text = f'{{"text": "{alert_message}"}}'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                url=str(settings.MATTERMOST_WEBHOOK_URL),
                data=text,
            ):
                logger.info(f"Successfully send test alert")
                return "Successfully send test alert"
        except Exception as err:
            logger.error(f"Sending test alert failed due to following errors: {err}")
            raise HTTPException(
                status_code=500, detail="Can`t connect to mattermost instance"
            )
