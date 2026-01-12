"""
Publisher CRUD
==============
CRUD операции для модели Publisher
"""

from typing import Optional, List
from sqlalchemy.orm import Session, selectinload
from app.crud.base import BaseCRUD
from app.models.publisher import Publisher


class PublisherCRUD(BaseCRUD[Publisher]):
    """
    CRUD операции для издательств.
    """

    def __init__(self):
        super().__init__(Publisher)

    def get_by_name(self, db: Session, name: str) -> Optional[Publisher]:
        """
        Найти издательство по названию.

        Args:
            db: Сессия базы данных
            name: Название издательства

        Returns:
            Издательство или None
        """
        return db.query(Publisher).filter(Publisher.name == name).first()

    def search_by_name(self, db: Session, name: str) -> List[Publisher]:
        """
        Поиск издательств по части названия.

        Args:
            db: Сессия базы данных
            name: Часть названия

        Returns:
            Список издательств
        """
        return db.query(Publisher).filter(
            Publisher.name.ilike(f"%{name}%")
        ).all()

    def get_with_books(self, db: Session, publisher_id: int) -> Optional[Publisher]:
        """
        Получить издательство со всеми книгами.

        Args:
            db: Сессия базы данных
            publisher_id: ID издательства

        Returns:
            Издательство с книгами или None
        """
        return db.query(Publisher).options(
            selectinload(Publisher.books)
        ).filter(Publisher.id == publisher_id).first()

    def get_publishers_stats(self, db: Session) -> List[tuple]:
        """
        Получить статистику по издательствам.

        Returns:
            Список кортежей (publisher_name, book_count, avg_price)
        """
        from sqlalchemy import func
        from app.models.book import Book

        return db.query(
            Publisher.name,
            func.count(Book.id).label("book_count"),
            func.avg(Book.price).label("avg_price")
        ).outerjoin(Book).group_by(
            Publisher.id, Publisher.name
        ).order_by(
            func.count(Book.id).desc()
        ).all()


# Синглтон для удобства использования
publisher_crud = PublisherCRUD()

