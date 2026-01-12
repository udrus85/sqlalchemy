"""
CRUD module - Create, Read, Update, Delete operations
======================================================
Классы для работы с базой данных
"""

from app.crud.base import BaseCRUD
from app.crud.author import AuthorCRUD, author_crud
from app.crud.book import BookCRUD, book_crud
from app.crud.genre import GenreCRUD, genre_crud
from app.crud.publisher import PublisherCRUD, publisher_crud

__all__ = [
    "BaseCRUD",
    "AuthorCRUD",
    "BookCRUD",
    "GenreCRUD",
    "PublisherCRUD",
    "author_crud",
    "book_crud",
    "genre_crud",
    "publisher_crud",
]

