from abc import ABC, abstractmethod
from typing import Any, Sequence

from apps.items.schemas import ItemCreate, ItemPatch, ItemRead, ItemUpdate


class ItemRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, item: ItemCreate) -> ItemRead:
        pass

    @abstractmethod
    async def read_all(self, skip: int = 0, limit: int = 100) -> Sequence[ItemRead]:
        pass

    @abstractmethod
    async def read_by_field(self, field: str, value: Any) -> ItemRead | None:
        pass

    @staticmethod
    def validate_field(field: str) -> None:
        if field not in ItemRead.model_fields:
            raise ValueError(f"Invalid field: {field}")

    @abstractmethod
    async def update(self, item_id: int, item_data: ItemUpdate) -> ItemRead | None:
        pass

    @abstractmethod
    async def patch(self, item_id: int, item_data: ItemPatch) -> ItemRead | None:
        pass

    @abstractmethod
    async def delete(self, item_id: int) -> ItemRead | None:
        pass
