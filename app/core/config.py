from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

import os

print(os.getcwd())  # покажет рабочую директорию
print(BASE_DIR / ".env", (BASE_DIR / ".env").exists())


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8010


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class ApiV1Prefix(BaseModel):
    # prefix: str = "/api"
    cat: str = "/cat"
    mission: str = "/mission"



class ApiPrefix(BaseModel):
    # prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="allow",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()

    db: DataBaseConfig
    # auth config
    SECRET_KEY: str
    ALGORITHM: str



settings = Settings()


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}
