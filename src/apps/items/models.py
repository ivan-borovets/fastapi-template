from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import AutoTableNameMixin, IntIdPkMixin, TimestampMixin


class Item(AutoTableNameMixin, IntIdPkMixin, TimestampMixin, Base):
    title: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column()
    price: Mapped[Decimal] = mapped_column(nullable=False)
    is_available: Mapped[bool] = mapped_column(default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Item(id={self.id}, title='{self.title}', price={self.price})>"
