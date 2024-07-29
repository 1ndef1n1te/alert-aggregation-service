from ..settings import settings
import aiofiles


async def init_data():
    for env in settings.ENVIRONMENTS.split(" "):
        async with aiofiles.open(f"./data/alerts-{env}.md", mode="w"):
            pass
