from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Query

from apps.items.dependencies import get_item_service
from apps.items.schemas import ItemCreate, ItemPatch, ItemRead, ItemUpdate
from apps.items.services import ItemService
from core.settings import settings

router = APIRouter(
    prefix=settings.api.v1.items_prefix,
    tags=list(settings.api.v1.items_tags),
)


@router.post(path="/", response_model=ItemRead)
async def create_item(
    service: Annotated[ItemService, Depends(get_item_service)],
    item: ItemCreate,
):
    return await service.create_item(item=item)


@router.get(path="/", response_model=Sequence[ItemRead])
async def get_all_items(
    service: Annotated[ItemService, Depends(get_item_service)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return await service.get_all_items(skip=skip, limit=limit)


@router.get(path="/{item_id}", response_model=ItemRead)
async def get_item_by_id(
    service: Annotated[ItemService, Depends(get_item_service)],
    item_id: int,
):
    return await service.get_item_by_id(item_id=item_id)


@router.get(path="/title/{title}", response_model=ItemRead)
async def get_item_by_title(
    service: Annotated[ItemService, Depends(get_item_service)],
    title: str,
):
    return await service.get_item_by_title(title=title)


@router.put(path="/{item_id}", response_model=ItemRead)
async def update_item(
    service: Annotated[ItemService, Depends(get_item_service)],
    item_id: int,
    item: ItemUpdate,
):
    return await service.update_item(item_id=item_id, item_data=item)


@router.patch(path="/{item_id}", response_model=ItemRead)
async def patch_item(
    service: Annotated[ItemService, Depends(get_item_service)],
    item_id: int,
    item: ItemPatch,
):
    return await service.patch_item(item_id=item_id, item_data=item)


@router.delete(path="/{item_id}", response_model=ItemRead)
async def delete_item(
    service: Annotated[ItemService, Depends(get_item_service)],
    item_id: int,
):
    return await service.delete_item(item_id=item_id)


@router.post(path="/{item_id}/toggle", response_model=ItemRead)
async def toggle_item_availability(
    service: Annotated[ItemService, Depends(get_item_service)],
    item_id: int,
):
    return await service.toggle_item_availability(item_id=item_id)
