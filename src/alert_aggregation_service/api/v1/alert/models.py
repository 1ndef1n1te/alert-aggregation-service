from pydantic import BaseModel
from enum import Enum


class Environment(str, Enum):
    environment1 = "environment1"
    environment2 = "environment2"


class Alert(BaseModel):
    name: str
    message: str
    env: Environment
