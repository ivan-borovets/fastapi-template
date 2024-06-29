from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from apps.items.repositories.sqla import ItemRepository
from apps.items.schemas import ItemCreate, ItemPatch, ItemRead, ItemUpdate


class ItemService:
    def __init__(self, session: AsyncSession):
        self.repository = ItemRepository(session=session)

    async def create_item(self, item: ItemCreate) -> ItemRead:
        try:
            return await self.repository.create(item=item)
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve)
            ) from ve

    async def get_all_items(
        self, skip: int = 0, limit: int = 100
    ) -> Sequence[ItemRead]:
        return await self.repository.read_all(skip=skip, limit=limit)

    async def get_item_by_id(self, item_id: int) -> ItemRead:
        item = await self.repository.read_by_field(field="id", value=item_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return item

    async def get_item_by_title(self, title: str) -> ItemRead:
        item = await self.repository.read_by_field(field="title", value=title)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return item

    async def update_item(self, item_id: int, item_data: ItemUpdate) -> ItemRead:
        try:
            updated_item = await self.repository.update(
                item_id=item_id, item_data=item_data
            )
            if updated_item is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
                )
            return updated_item
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(ve)
            ) from ve

    async def patch_item(self, item_id: int, item_data: ItemPatch) -> ItemRead:
        try:
            updated_item = await self.repository.patch(
                item_id=item_id, item_data=item_data
            )
            if updated_item is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
                )
            return updated_item
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve)
            ) from ve

    async def delete_item(self, item_id: int) -> ItemRead:
        deleted_item = await self.repository.delete(item_id=item_id)
        if deleted_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return deleted_item

    async def toggle_item_availability(self, item_id: int) -> ItemRead:
        item = await self.repository.read_by_field(field="id", value=item_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        update_data = ItemUpdate(is_available=not item.is_available)
        updated_item = await self.repository.update(
            item_id=item_id, item_data=update_data
        )

        if updated_item is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update item",
            )

        return updated_item
