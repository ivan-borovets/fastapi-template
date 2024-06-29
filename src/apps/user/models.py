from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import AutoTableNameMixin, IntIdPkMixin


class User(AutoTableNameMixin, IntIdPkMixin, Base):
    username: Mapped[str] = mapped_column(unique=True)
