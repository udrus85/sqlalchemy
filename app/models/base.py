"""
        return f"<{self.__class__.__name__}(id={self.id})>"
    def __repr__(self):

    )
        nullable=False
        onupdate=datetime.utcnow,
        default=datetime.utcnow,
        DateTime,
    updated_at = Column(
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    __abstract__ = True
    """
    Содержит общие поля: id, created_at, updated_at
    Абстрактная базовая модель.
    """
class BaseModel(Base):


from app.core.database import Base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

"""
Базовая модель с общими полями для всех сущностей
==========
Base Model

