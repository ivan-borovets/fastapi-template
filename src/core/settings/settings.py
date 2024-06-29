from pathlib import Path

import rtoml
from pydantic import Field, PostgresDsn, computed_field

from core.settings.api_literals import ApiLiteral
from core.settings.docker_env import DockerEnv
from core.settings.get_base_dir import get_base_dir
from core.settings.settings_model import SettingsModel


class Structure(SettingsModel):
    src_dir: str = Field(alias="SRC_DIR")
    tests_dir: str = Field(alias="TESTS_DIR")
    pyproject_toml: str = Field(alias="PYPROJECT_TOML")


class Run(SettingsModel):
    host: str = Field(alias="UVICORN_HOST")
    port: int = Field(alias="UVICORN_PORT")
    reload: bool = Field(alias="UVICORN_RELOAD")


class DbPostgres(SettingsModel):
    username: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    path: str = Field(alias="POSTGRES_DB")

    @computed_field  # type: ignore
    @property
    def url(self) -> str:
        """Generate PostgreSQL DSN."""
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


class Settings(SettingsModel):
    structure: Structure
    run: Run
    db: Db
    api: ApiLiteral = ApiLiteral()


def toml_to_dict(config_path: str) -> dict:
    with open(config_path, mode="r", encoding="utf-8") as f:
        toml_dict: dict = rtoml.load(f)
    return toml_dict


def create_settings() -> Settings:
    base_dir: Path = get_base_dir()
    config_path: Path = base_dir / "config.toml"
    toml_dict: dict = toml_to_dict(config_path=str(config_path))
    if not DockerEnv().is_docker:  # type: ignore
        toml_dict["db"]["postgres"]["POSTGRES_HOST"] = "localhost"
    app_settings: Settings = Settings.parse_obj(toml_dict)
    return app_settings


settings: Settings = create_settings()

if __name__ == "__main__":
    print(settings.db.postgres.host)
