import enum
from pathlib import Path
from tempfile import gettempdir

import pydantic
#from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL
from pydantic import BaseModel
TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(pydantic.BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "0.0.0.0"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = True

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_host: str = "poc-db"
    db_port: int = 5432
    db_user: str = "poc"
    db_pass: str = "poc"
    db_base: str = "poc"
    db_echo: bool = True

    @property
    def db_url_sync(self) -> URL:
        return URL.build(
            scheme="postgresql+psycopg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )


    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     env_prefix="POC_",
    #     env_file_encoding="utf-8",
    # )


settings = Settings()
