from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.user.repositories import all_users, new_user
from apps.user.schemas import UserCreate, UserRead
from core.dependencies import get_db_session
from core.settings import settings

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=list(settings.api.v1.users_tags),
)


@router.get(path="", response_model=list[UserRead])
async def get_users(session: Annotated[AsyncSession, Depends(get_db_session)]):
    users = await all_users(session=session)
    return users


@router.post(path="", response_model=UserRead)
async def create_user(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user_create: UserCreate,
):
    user = await new_user(session=session, user_create=user_create)
    return user
