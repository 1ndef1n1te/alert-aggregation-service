from pydantic_settings import BaseSettings
from pydantic import HttpUrl


class Settings(BaseSettings):
    MATTERMOST_WEBHOOK_URL: HttpUrl

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
