from pydantic import BaseModel, ConfigDict


class SettingsModel(BaseModel):
    model_config = ConfigDict(frozen=True)
