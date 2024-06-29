from enum import Enum

from core.settings.settings_model import SettingsModel


class ApiV1Literal(SettingsModel):
    prefix: str = "/v1"
    users: str = "/users"
    users_tags: tuple[str | Enum] = ("Users",)


class ApiLiteral(SettingsModel):
    prefix: str = "/api"
    v1: ApiV1Literal = ApiV1Literal()
