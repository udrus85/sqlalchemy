"""
Publisher Model
===============
Модель издательства
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Publisher(BaseModel):
    """
    Модель издательства.

    Связи:
    - One-to-Many с Book (одно издательство выпускает много книг)

    Attributes:
        name: Название издательства
        address: Адрес
        website: Веб-сайт
        description: Описание
        books: Список книг издательства (relationship)
    """
    __tablename__ = "publishers"

    name = Column(String(255), nullable=False, unique=True, index=True)
    address = Column(String(500), nullable=True)
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    # One-to-Many relationship: Publisher -> Books
    books = relationship(
        "Book",
        back_populates="publisher",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}')>"

