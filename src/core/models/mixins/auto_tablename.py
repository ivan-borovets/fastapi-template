from camelsnake import camel_to_snake
from sqlalchemy.orm import declared_attr


class AutoTableNameMixin:
    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_to_snake(cls.__name__)}s"
