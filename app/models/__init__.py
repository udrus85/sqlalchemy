"""
Models module - SQLAlchemy ORM models
======================================
Модели данных для книжного каталога
"""

from app.models.base import BaseModel
from app.models.author import Author
from app.models.publisher import Publisher
from app.models.genre import Genre
from app.models.book import Book, book_genres

__all__ = [
    "BaseModel",
    "Author",
    "Publisher",
    "Genre",
    "Book",
    "book_genres"
]

