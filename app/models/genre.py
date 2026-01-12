"""
Genre Model
===========
Модель жанра книги
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Genre(BaseModel):
    """
    Модель жанра.

    Связи:
    - Many-to-Many с Book (один жанр у многих книг, одна книга в нескольких жанрах)

    Attributes:
        name: Название жанра
        description: Описание жанра
        books: Список книг этого жанра (relationship через association table)
    """
    __tablename__ = "genres"

    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    # Many-to-Many relationship: Genre <-> Books
    # secondary указывает на ассоциативную таблицу
    books = relationship(
        "Book",
        secondary="book_genres",  # Имя ассоциативной таблицы
        back_populates="genres",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"

