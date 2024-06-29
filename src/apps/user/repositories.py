from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.user.models import User
from apps.user.schemas import UserCreate


async def all_users(session: AsyncSession) -> Sequence[User]:
    statement = select(User).order_by(User.id)
    result = await session.scalars(statement=statement)
    return result.all()


async def new_user(session: AsyncSession, user_create: UserCreate) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
