"""
Book CRUD
=========
CRUD операции для модели Book
"""

from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_, or_
from app.crud.base import BaseCRUD
from app.models.book import Book
from app.models.genre import Genre


class BookCRUD(BaseCRUD[Book]):
    """
    CRUD операции для книг.

    Расширяет базовый CRUD специфичными методами для Book.
    """

    def __init__(self):
        super().__init__(Book)

    def get_by_isbn(self, db: Session, isbn: str) -> Optional[Book]:
        """
        Найти книгу по ISBN.

        Args:
            db: Сессия базы данных
            isbn: ISBN номер книги

        Returns:
            Книга или None
        """
        return db.query(Book).filter(Book.isbn == isbn).first()

    def search_by_title(self, db: Session, title: str) -> List[Book]:
        """
        Поиск книг по названию (LIKE).

        Args:
            db: Сессия базы данных
            title: Часть названия для поиска

        Returns:
            Список книг
        """
        return db.query(Book).filter(
            Book.title.ilike(f"%{title}%")
        ).all()

    def get_by_author(
        self,
        db: Session,
        author_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Book]:
        """
        Получить книги автора.

        Args:
            db: Сессия базы данных
            author_id: ID автора
            skip: Пропустить записей
            limit: Лимит записей

        Returns:
            Список книг автора
        """
        return db.query(Book).filter(
            Book.author_id == author_id
        ).offset(skip).limit(limit).all()

    def get_by_genre(self, db: Session, genre_id: int) -> List[Book]:
        """
        Получить книги по жанру (Many-to-Many).

        Args:
            db: Сессия базы данных
            genre_id: ID жанра

        Returns:
            Список книг в этом жанре
        """
        return db.query(Book).join(Book.genres).filter(
            Genre.id == genre_id
        ).all()

    def get_by_price_range(
        self,
        db: Session,
        min_price: float = 0,
        max_price: float = float('inf')
    ) -> List[Book]:
        """
        Получить книги в ценовом диапазоне.

        Args:
            db: Сессия базы данных
            min_price: Минимальная цена
            max_price: Максимальная цена

        Returns:
            Список книг
        """
        return db.query(Book).filter(
            and_(
                Book.price >= min_price,
                Book.price <= max_price
            )
        ).all()

    def get_published_between(
        self,
        db: Session,
        start_date: date,
        end_date: date
    ) -> List[Book]:
        """
        Получить книги, изданные в указанный период.

        Args:
            db: Сессия базы данных
            start_date: Начальная дата
            end_date: Конечная дата

        Returns:
            Список книг
        """
        return db.query(Book).filter(
            and_(
                Book.publication_date >= start_date,
                Book.publication_date <= end_date
            )
        ).all()

    def get_with_relations(self, db: Session, book_id: int) -> Optional[Book]:
        """
        Получить книгу со всеми связями (author, publisher, genres).
        Оптимизировано с помощью selectinload.

        Args:
            db: Сессия базы данных
            book_id: ID книги

        Returns:
            Книга с загруженными связями или None
        """
        return db.query(Book).options(
            selectinload(Book.author),
            selectinload(Book.publisher),
            selectinload(Book.genres)
        ).filter(Book.id == book_id).first()

    def add_genre_to_book(
        self,
        db: Session,
        book_id: int,
        genre_id: int
    ) -> Optional[Book]:
        """
        Добавить жанр к книге (Many-to-Many).

        Args:
            db: Сессия базы данных
            book_id: ID книги
            genre_id: ID жанра

        Returns:
            Обновлённая книга или None
        """
        book = self.get_with_relations(db, book_id)
        if book is None:
            return None

        genre = db.query(Genre).filter(Genre.id == genre_id).first()
        if genre is None:
            return None

        if genre not in book.genres:
            book.genres.append(genre)
            db.commit()
            db.refresh(book)

        return book

    def remove_genre_from_book(
        self,
        db: Session,
        book_id: int,
        genre_id: int
    ) -> Optional[Book]:
        """
        Удалить жанр из книги.

        Args:
            db: Сессия базы данных
            book_id: ID книги
            genre_id: ID жанра

        Returns:
            Обновлённая книга или None
        """
        book = self.get_with_relations(db, book_id)
        if book is None:
            return None

        genre = db.query(Genre).filter(Genre.id == genre_id).first()
        if genre and genre in book.genres:
            book.genres.remove(genre)
            db.commit()
            db.refresh(book)

        return book

    def advanced_search(
        self,
        db: Session,
        title: Optional[str] = None,
        author_name: Optional[str] = None,
        genre_name: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        language: Optional[str] = None
    ) -> List[Book]:
        """
        Расширенный поиск книг с несколькими фильтрами.

        Демонстрирует построение динамических запросов.

        Args:
            db: Сессия базы данных
            title: Часть названия
            author_name: Часть имени автора
            genre_name: Название жанра
            min_price: Минимальная цена
            max_price: Максимальная цена
            language: Язык книги

        Returns:
            Список книг, соответствующих критериям
        """
        from app.models.author import Author

        query = db.query(Book)

        # Динамически добавляем фильтры
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))

        if author_name:
            query = query.join(Author).filter(
                Author.name.ilike(f"%{author_name}%")
            )

        if genre_name:
            query = query.join(Book.genres).filter(
                Genre.name.ilike(f"%{genre_name}%")
            )

        if min_price is not None:
            query = query.filter(Book.price >= min_price)

        if max_price is not None:
            query = query.filter(Book.price <= max_price)

        if language:
            query = query.filter(Book.language == language)

        return query.all()


# Синглтон для удобства использования
book_crud = BookCRUD()

