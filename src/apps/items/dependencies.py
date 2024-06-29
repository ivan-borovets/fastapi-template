from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.items.services import ItemService
from core.dependencies import get_db_session


async def get_item_service(
    session: AsyncSession = Depends(get_db_session),
) -> ItemService:
    return ItemService(session=session)
