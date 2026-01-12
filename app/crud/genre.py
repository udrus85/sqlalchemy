"""
Genre CRUD
==========
CRUD операции для модели Genre
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import BaseCRUD
from app.models.genre import Genre


class GenreCRUD(BaseCRUD[Genre]):
    """
    CRUD операции для жанров.
    """

    def __init__(self):
        super().__init__(Genre)

    def get_by_name(self, db: Session, name: str) -> Optional[Genre]:
        """
        Найти жанр по названию.

        Args:
            db: Сессия базы данных
            name: Название жанра

        Returns:
            Жанр или None
        """
        return db.query(Genre).filter(Genre.name == name).first()

    def get_or_create(self, db: Session, name: str, description: str = None) -> Genre:
        """
        Получить жанр или создать новый, если не существует.

        Args:
            db: Сессия базы данных
            name: Название жанра
            description: Описание жанра

        Returns:
            Жанр (существующий или созданный)
        """
        genre = self.get_by_name(db, name)
        if genre:
            return genre
        return self.create(db, name=name, description=description)

    def get_popular_genres(self, db: Session, limit: int = 10) -> List[tuple]:
        """
        Получить самые популярные жанры по количеству книг.

        Args:
            db: Сессия базы данных
            limit: Максимальное количество жанров

        Returns:
            Список кортежей (genre_name, book_count)
        """
        from sqlalchemy import func
        from app.models.book import Book, book_genres

        return db.query(
            Genre.name,
            func.count(book_genres.c.book_id).label("book_count")
        ).outerjoin(book_genres).group_by(
            Genre.id, Genre.name
        ).order_by(
            func.count(book_genres.c.book_id).desc()
        ).limit(limit).all()


# Синглтон для удобства использования
genre_crud = GenreCRUD()

