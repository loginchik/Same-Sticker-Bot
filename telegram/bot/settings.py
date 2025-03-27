from os import getenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = getenv("BOT_TOKEN")


settings = Settings()