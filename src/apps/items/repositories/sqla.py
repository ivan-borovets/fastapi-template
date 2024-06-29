from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.items.models import Item
from apps.items.repositories.abstract import ItemRepositoryInterface
from apps.items.schemas import ItemCreate, ItemPatch, ItemRead, ItemUpdate


class ItemRepository(ItemRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, item: ItemCreate) -> ItemRead:
        db_item = Item(**item.model_dump())
        self.session.add(db_item)
        try:
            await self.session.commit()
            await self.session.refresh(db_item)
        except IntegrityError as ie:
            await self.session.rollback()
            raise ValueError("An item with this title already exists") from ie
        return ItemRead.model_validate(db_item)

    async def read_all(self, skip: int = 0, limit: int = 100) -> Sequence[ItemRead]:
        query = select(Item).offset(skip).limit(limit).order_by(Item.id)
        result = await self.session.execute(query)
        items = result.scalars().all()
        return [ItemRead.model_validate(item) for item in items]

    async def read_by_field(self, field: str, value: Any) -> ItemRead | None:
        self.validate_field(field)
        # noinspection PyTypeChecker
        query = select(Item).filter(getattr(Item, field) == value)
        result = await self.session.execute(query)
        item = result.scalar_one_or_none()
        return ItemRead.model_validate(item) if item else None

    async def update(self, item_id: int, item_data: ItemUpdate) -> ItemRead | None:
        query = select(Item).where(Item.id == item_id)
        result = await self.session.execute(query)
        db_item = result.scalar_one_or_none()
        if db_item is None:
            return None

        for field, value in item_data.model_dump(exclude_unset=True).items():
            setattr(db_item, field, value)

        try:
            await self.session.commit()
            await self.session.refresh(db_item)
        except IntegrityError as ie:
            await self.session.rollback()
            raise ValueError("An item with this title already exists") from ie
        return ItemRead.model_validate(db_item)

    async def patch(self, item_id: int, item_data: ItemPatch) -> ItemRead | None:
        query = select(Item).where(Item.id == item_id)
        result = await self.session.execute(query)
        db_item = result.scalar_one_or_none()
        if db_item is None:
            return None

        for field, value in item_data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(db_item, field, value)

        try:
            await self.session.commit()
            await self.session.refresh(db_item)
        except IntegrityError as ie:
            await self.session.rollback()
            raise ValueError("An item with this title already exists") from ie
        return ItemRead.model_validate(db_item)

    async def delete(self, item_id: int) -> ItemRead | None:
        query = select(Item).where(Item.id == item_id)
        result = await self.session.execute(query)
        db_item = result.scalar_one_or_none()
        if db_item is None:
            return None

        await self.session.delete(db_item)
        await self.session.commit()
        return ItemRead.model_validate(db_item)
