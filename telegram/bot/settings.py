from os import getenv
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Project settings
    """

    BASE_DIR: Path = Path(__file__).resolve().parent

    BOT_TOKEN: str = getenv("BOT_TOKEN")


settings = Settings()
