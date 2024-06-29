from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from core.settings.settings import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=settings.db.sqlalchemy.naming_conventions)
