"""
Author Model
============
Модель автора книг
"""

from sqlalchemy import Column, String, Text, Date
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Author(BaseModel):
    """
    Модель автора.

    Связи:
    - One-to-Many с Book (у одного автора много книг)

    Attributes:
        name: Имя автора
        bio: Биография
        birth_date: Дата рождения
        country: Страна
        books: Список книг автора (relationship)
    """
    __tablename__ = "authors"

    name = Column(String(255), nullable=False, index=True)
    bio = Column(Text, nullable=True)
    birth_date = Column(Date, nullable=True)
    country = Column(String(100), nullable=True)

    # One-to-Many relationship: Author -> Books
    # back_populates создаёт двустороннюю связь
    books = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan",  # При удалении автора удаляются его книги
        lazy="selectin"  # Оптимизация: загрузка связанных объектов одним запросом
    )

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"

    @property
    def books_count(self) -> int:
        """Количество книг автора"""
        return len(self.books) if self.books else 0

