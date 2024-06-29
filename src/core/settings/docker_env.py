from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.settings.get_base_dir import get_base_dir


class DockerEnv(BaseSettings):
    is_docker: bool = Field(alias="IS_DOCKER")

    model_config = SettingsConfigDict(
        env_file=f"{get_base_dir()}/.env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )
