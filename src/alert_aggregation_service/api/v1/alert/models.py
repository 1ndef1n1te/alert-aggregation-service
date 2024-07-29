from pydantic import BaseModel
from enum import Enum
from ....settings import settings

custom_environments_dict = {k: k for k in settings.ENVIRONMENTS.split(" ")}

Environment = Enum("Environment", custom_environments_dict)


class Alert(BaseModel):
    name: str
    message: str
    env: Environment
