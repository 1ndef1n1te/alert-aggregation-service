from fastapi import APIRouter
from .models import Alert, Environment
from ....settings import settings
import aiofiles
import aiohttp
from loguru import logger
from fastapi.exceptions import HTTPException

alert_router = APIRouter(prefix="/api/v1/alert", tags=["alert"])


@alert_router.post("/create", summary="Add alert")
async def create_alert(alert: Alert):
    async with aiofiles.open(f"./data/alerts-{alert.env.value}.md", mode="a") as f:
        await f.write(f"|{alert.name:^25}|{alert.message:^25}|\n")
        logger.info(
            f"Successfully add alert: {alert.name} with message: {alert.message} | environment: {alert.env.value}"
        )
    return {"status": "ok"}


@alert_router.post("/send/{alert_env}", summary="Send alerts")
async def send_alert(alert_env: Environment):
    try:
        async with aiofiles.open(f"./data/alerts-{alert_env.value}.md", "r") as file:
            alerts = await file.readlines()
    except FileNotFoundError:
        logger.error(f"Can`t open alerts file | environment {alert_env.value}")
        raise HTTPException(
            status_code=500,
            detail=f"Can`t open alerts file | environment {alert_env.value}",
        )
    alerts.insert(0, f"### {alert_env.value} stand alerts\n")
    alerts.insert(1, f"|{'Alert name':^25}|{'Alert content':^25}|\n")
    alerts.insert(2, f"|{'-':^25}|{'-':^25}|\n")
    alert_message = "".join(alerts)
    text = f'{{"text": "{alert_message}"}}'
    if len(alerts) > 3:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=str(settings.MATTERMOST_WEBHOOK_URL),
                data=text,
            ):
                logger.info(
                    f"Successfully send: {len(alerts)-3} alerts to the reciever server | environment: {alert_env.value} "
                )
        async with aiofiles.open(f"./data/alerts-{alert_env.value}.md", "w") as file:
            logger.info(f"Successfully clear alerts | environment: {alert_env.value}")
        return {"status": "ok"}
    else:
        logger.info(f"There are no alerts  skipping... | environment {alert_env.value}")
        raise HTTPException(
            status_code=200,
            detail=f"There are no alerts skipping... | environment: {alert_env.value}",
        )


@alert_router.get("/list/{alert_env}", summary="List alerts for specific environment")
async def list_alerts(alert_env: Environment):
    alerts_list = []
    try:
        async with aiofiles.open(
            f"./data/alerts-{alert_env.value}.md", mode="r"
        ) as file:
            alerts = await file.readlines()
            for alert in alerts:
                alert = alert.strip("|").strip("\n").split("|")
                alert = Alert(name=alert[0].strip(), message=alert[1].strip(), env=alert_env.value)
                alerts_list.append(alert)
        return alerts_list
    except FileNotFoundError:
        logger.error(f"Can`t open alerts file | environment {alert_env.value}")
        raise HTTPException(
            status_code=500,
            detail=f"Can`t open alerts file | environment {alert_env.value}",
        )


@alert_router.delete(
    "/clear/{alert_env}", summary="Clear alert for specific environment"
)
async def clear_alerts(alert_env: Environment):
    async with aiofiles.open(f"./data/alerts-{alert_env.value}.md", mode="w") as f:
        logger.info(f"Successfully clear alerts | environment: {alert_env.value}")
        return {"status": "ok"}
