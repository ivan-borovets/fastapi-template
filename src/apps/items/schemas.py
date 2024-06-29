from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ItemBase(ORMBaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str | None = Field(None, max_length=1000)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    is_available: bool = True


class ItemCreate(ItemBase):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Example Item",
                "description": "An example item.",
                "price": 19.99,
                "is_available": True,
            }
        }
    )


class ItemRead(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Example Item",
                "description": "An example item.",
                "price": 19.99,
                "is_available": True,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            }
        }
    )


class ItemUpdate(ORMBaseModel):
    title: str | None = Field(None, min_length=3, max_length=200)
    description: str | None = Field(None, max_length=1000)
    price: Decimal | None = Field(None, gt=0, decimal_places=2)
    is_available: bool | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated Item",
                "description": "An updated description.",
                "price": 29.99,
                "is_available": False,
            }
        }
    )


class ItemPatch(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=200)
    description: str | None = Field(None, max_length=1000)
    price: Decimal | None = Field(None, gt=0, decimal_places=2)
    is_available: bool | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": None,
                "description": None,
                "price": 19.99,
                "is_available": None,
            }
        }
    )
