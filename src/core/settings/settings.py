from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import rtoml
from pydantic import BaseModel, ConfigDict, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class Structure(SettingsModel):
    src_dir: str = Field(alias="SRC_DIR")
    tests_dir: str = Field(alias="TESTS_DIR")
    pyproject_toml: str = Field(alias="PYPROJECT_TOML")


class DbPostgres(SettingsModel):
    username: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    path: str = Field(alias="POSTGRES_DB")

    @property
    def url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.path,
            )
        )


class DbSqlalchemy(SettingsModel):
    echo: bool = Field(alias="SQLA_ECHO")
    echo_pool: bool = Field(alias="SQLA_ECHO_POOL")
    pool_size: int = Field(alias="SQLA_POOL_SIZE")
    max_overflow: int = Field(alias="SQLA_MAX_OVERFLOW")

    naming_conventions: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Db(SettingsModel):
    postgres: DbPostgres
    sqlalchemy: DbSqlalchemy


class Run(SettingsModel):
    host: str = Field(alias="UVICORN_HOST")
    port: int = Field(alias="UVICORN_PORT")
    reload: bool = Field(alias="UVICORN_RELOAD")


class ApiV1Literal(SettingsModel):
    prefix: str = Field(alias="API_V1_PREFIX")
    items_prefix: str = Field(alias="API_V1_ITEMS_PREFIX")
    items_tags: tuple[str] = Field(alias="API_V1_ITEMS_TAGS")


class ApiLiteral(SettingsModel):
    prefix: str = Field(alias="API_PREFIX")
    v1: ApiV1Literal


class Dotenv(BaseSettings):
    is_docker: bool = Field(alias="IS_DOCKER")

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8", extra="ignore", case_sensitive=False, frozen=True
    )

    @classmethod
    def from_file(cls, path: Path) -> Dotenv:
        if not path.is_file():
            raise FileNotFoundError(
                f"The file does not exist at the specified path: {path}"
            )
        instance: Dotenv = cls(_env_file=str(path))
        instance.model_config["env_file"] = str(path)
        return instance


class Settings(SettingsModel):
    structure: Structure
    db: Db
    run: Run
    api: ApiLiteral

    @staticmethod
    def _toml_to_dict(path: Path) -> dict:
        with open(path, mode="r", encoding="utf-8") as f:
            toml_dict: dict = rtoml.load(f)
        return toml_dict

    @classmethod
    def from_file(cls, path: Path, is_docker: bool) -> Settings:
        if not path.is_file():
            raise FileNotFoundError(
                f"The file does not exist at the specified path: {path}"
            )
        toml_dict: dict = cls._toml_to_dict(path=path)
        if not is_docker:
            toml_dict["db"]["postgres"]["POSTGRES_HOST"] = "localhost"
        instance: Settings = cls.model_validate(toml_dict)
        return instance


@lru_cache(maxsize=1)
def create_settings() -> Settings:
    base_dir: Path = Path(__file__).parent.parent.parent.parent
    toml_path: Path = base_dir / "config.toml"
    dotenv_path: Path = base_dir / ".env"

    dotenv: Dotenv = Dotenv.from_file(path=dotenv_path)
    settings_created: Settings = Settings.from_file(
        path=toml_path, is_docker=dotenv.is_docker
    )
    return settings_created


settings: Settings = create_settings()
