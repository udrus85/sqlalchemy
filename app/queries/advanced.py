"""
Advanced Queries
================
Демонстрация продвинутых SQL запросов с SQLAlchemy
"""

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc, case, and_, or_, text
from sqlalchemy.sql import label

from app.models.author import Author
from app.models.book import Book, book_genres
from app.models.genre import Genre
from app.models.publisher import Publisher


class AdvancedQueries:
    """
    Класс с продвинутыми запросами для демонстрации возможностей SQLAlchemy.

    Включает:
    - Агрегатные функции (COUNT, SUM, AVG, MAX, MIN)
    - GROUP BY и HAVING
    - JOIN (INNER, LEFT, RIGHT, OUTER)
    - Подзапросы (Subqueries)
    - Оконные функции (Window Functions)
    - Условная логика (CASE WHEN)
    - Сортировка и пагинация
    """

    # ==================== АГРЕГАТНЫЕ ФУНКЦИИ ====================

    @staticmethod
    def get_library_statistics(db: Session) -> dict:
        """
        Получить общую статистику библиотеки.
        Демонстрирует использование агрегатных функций.

        Returns:
            Словарь со статистикой
        """
        stats = db.query(
            func.count(Book.id).label("total_books"),
            func.count(func.distinct(Book.author_id)).label("total_authors"),
            func.avg(Book.price).label("avg_price"),
            func.max(Book.price).label("max_price"),
            func.min(Book.price).label("min_price"),
            func.sum(Book.pages).label("total_pages")
        ).first()

        return {
            "total_books": stats.total_books or 0,
            "total_authors": stats.total_authors or 0,
            "avg_price": round(float(stats.avg_price or 0), 2),
            "max_price": float(stats.max_price or 0),
            "min_price": float(stats.min_price or 0),
            "total_pages": stats.total_pages or 0
        }

    # ==================== GROUP BY И HAVING ====================

    @staticmethod
    def get_books_count_by_language(db: Session) -> List[tuple]:
        """
        Количество книг по языкам.
        Демонстрирует GROUP BY.

        Returns:
            Список кортежей (язык, количество)
        """
        return db.query(
            Book.language,
            func.count(Book.id).label("count")
        ).group_by(Book.language).order_by(
            desc("count")
        ).all()

    @staticmethod
    def get_prolific_authors(db: Session, min_books: int = 3) -> List[tuple]:
        """
        Авторы с минимальным количеством книг.
        Демонстрирует GROUP BY + HAVING.

        Args:
            min_books: Минимальное количество книг

        Returns:
            Список кортежей (имя автора, количество книг)
        """
        return db.query(
            Author.name,
            func.count(Book.id).label("book_count")
        ).join(Book).group_by(
            Author.id, Author.name
        ).having(
            func.count(Book.id) >= min_books
        ).order_by(
            desc("book_count")
        ).all()

    @staticmethod
    def get_genre_statistics(db: Session) -> List[dict]:
        """
        Статистика по жанрам: количество книг, средняя цена, общее число страниц.

        Returns:
            Список словарей со статистикой по жанрам
        """
        results = db.query(
            Genre.name.label("genre"),
            func.count(Book.id).label("book_count"),
            func.avg(Book.price).label("avg_price"),
            func.sum(Book.pages).label("total_pages")
        ).join(
            book_genres, Genre.id == book_genres.c.genre_id
        ).join(
            Book, Book.id == book_genres.c.book_id
        ).group_by(
            Genre.id, Genre.name
        ).order_by(
            desc("book_count")
        ).all()

        return [
            {
                "genre": r.genre,
                "book_count": r.book_count,
                "avg_price": round(float(r.avg_price or 0), 2),
                "total_pages": r.total_pages or 0
            }
            for r in results
        ]

    # ==================== JOIN ЗАПРОСЫ ====================

    @staticmethod
    def get_books_with_author_and_publisher(
        db: Session,
        skip: int = 0,
        limit: int = 20
    ) -> List[dict]:
        """
        Получить книги с информацией об авторе и издательстве.
        Демонстрирует INNER JOIN и LEFT JOIN.

        Returns:
            Список словарей с информацией о книгах
        """
        results = db.query(
            Book.title,
            Book.price,
            Author.name.label("author_name"),
            Publisher.name.label("publisher_name")
        ).join(
            Author, Book.author_id == Author.id  # INNER JOIN
        ).outerjoin(
            Publisher, Book.publisher_id == Publisher.id  # LEFT JOIN
        ).offset(skip).limit(limit).all()

        return [
            {
                "title": r.title,
                "price": r.price,
                "author": r.author_name,
                "publisher": r.publisher_name or "Неизвестно"
            }
            for r in results
        ]

    @staticmethod
    def get_authors_without_books(db: Session) -> List[Author]:
        """
        Авторы без книг.
        Демонстрирует LEFT JOIN + IS NULL.

        Returns:
            Список авторов
        """
        return db.query(Author).outerjoin(Book).filter(
            Book.id == None
        ).all()

    # ==================== ПОДЗАПРОСЫ ====================

    @staticmethod
    def get_books_above_average_price(db: Session) -> List[Book]:
        """
        Книги с ценой выше средней.
        Демонстрирует использование подзапроса.

        Returns:
            Список книг
        """
        # Подзапрос для вычисления средней цены
        avg_price_subquery = db.query(
            func.avg(Book.price)
        ).scalar_subquery()

        return db.query(Book).filter(
            Book.price > avg_price_subquery
        ).all()

    @staticmethod
    def get_authors_with_expensive_books(
        db: Session,
        price_threshold: float = 1000
    ) -> List[tuple]:
        """
        Авторы, у которых есть хотя бы одна дорогая книга.
        Демонстрирует EXISTS с подзапросом.

        Returns:
            Список кортежей (имя автора, макс. цена книги)
        """
        from sqlalchemy import exists

        # Подзапрос: существует книга этого автора с ценой выше порога
        expensive_book_exists = exists().where(
            and_(
                Book.author_id == Author.id,
                Book.price >= price_threshold
            )
        )

        return db.query(
            Author.name,
            func.max(Book.price).label("max_book_price")
        ).join(Book).filter(
            expensive_book_exists
        ).group_by(Author.id, Author.name).all()

    # ==================== УСЛОВНАЯ ЛОГИКА (CASE) ====================

    @staticmethod
    def get_books_with_price_category(db: Session) -> List[dict]:
        """
        Книги с категорией цены.
        Демонстрирует CASE WHEN.

        Returns:
            Список словарей с книгами и категориями
        """
        price_category = case(
            (Book.price < 300, "Бюджетная"),
            (Book.price < 700, "Средняя"),
            (Book.price < 1500, "Дорогая"),
            else_="Премиум"
        ).label("price_category")

        results = db.query(
            Book.title,
            Book.price,
            price_category
        ).order_by(Book.price).all()

        return [
            {
                "title": r.title,
                "price": r.price,
                "category": r.price_category
            }
            for r in results
        ]

    @staticmethod
    def get_author_rating_by_books(db: Session) -> List[dict]:
        """
        Рейтинг авторов на основе количества книг.
        Демонстрирует CASE с агрегацией.

        Returns:
            Список словарей с авторами и рейтингами
        """
        book_count = func.count(Book.id)

        rating = case(
            (book_count >= 10, "Мастер"),
            (book_count >= 5, "Опытный"),
            (book_count >= 2, "Начинающий"),
            else_="Дебютант"
        ).label("rating")

        results = db.query(
            Author.name,
            book_count.label("book_count"),
            rating
        ).outerjoin(Book).group_by(
            Author.id, Author.name
        ).order_by(desc(book_count)).all()

        return [
            {
                "author": r.name,
                "book_count": r.book_count,
                "rating": r.rating
            }
            for r in results
        ]

    # ==================== СОРТИРОВКА И ПАГИНАЦИЯ ====================

    @staticmethod
    def get_books_sorted(
        db: Session,
        sort_by: str = "title",
        order: str = "asc",
        skip: int = 0,
        limit: int = 10
    ) -> List[Book]:
        """
        Получить книги с сортировкой и пагинацией.

        Args:
            sort_by: Поле для сортировки (title, price, pages, publication_date)
            order: Порядок сортировки (asc, desc)
            skip: Пропустить записей
            limit: Лимит записей

        Returns:
            Список книг
        """
        # Безопасное получение поля для сортировки
        sort_field = getattr(Book, sort_by, Book.title)

        if order.lower() == "desc":
            sort_field = desc(sort_field)
        else:
            sort_field = asc(sort_field)

        return db.query(Book).order_by(
            sort_field
        ).offset(skip).limit(limit).all()

    # ==================== RAW SQL ====================

    @staticmethod
    def execute_raw_sql(db: Session, sql: str, params: dict = None) -> List:
        """
        Выполнить сырой SQL-запрос.
        Полезно для сложных запросов, которые трудно выразить через ORM.

        Args:
            sql: SQL-запрос
            params: Параметры запроса

        Returns:
            Результат запроса

        Example:
            >>> result = AdvancedQueries.execute_raw_sql(
            ...     db,
            ...     "SELECT * FROM books WHERE price > :price",
            ...     {"price": 500}
            ... )
        """
        result = db.execute(text(sql), params or {})
        return result.fetchall()

    # ==================== КОМБИНИРОВАННЫЕ ЗАПРОСЫ ====================

    @staticmethod
    def get_dashboard_data(db: Session) -> dict:
        """
        Получить данные для дашборда - комплексный запрос.

        Returns:
            Словарь с данными для дашборда
        """
        # Общая статистика
        stats = AdvancedQueries.get_library_statistics(db)

        # Топ-5 авторов
        top_authors = db.query(
            Author.name,
            func.count(Book.id).label("count")
        ).join(Book).group_by(
            Author.id, Author.name
        ).order_by(
            desc("count")
        ).limit(5).all()

        # Топ-5 жанров
        top_genres = db.query(
            Genre.name,
            func.count(book_genres.c.book_id).label("count")
        ).outerjoin(book_genres).group_by(
            Genre.id, Genre.name
        ).order_by(
            desc("count")
        ).limit(5).all()

        # Последние добавленные книги
        recent_books = db.query(
            Book.title,
            Book.created_at
        ).order_by(
            desc(Book.created_at)
        ).limit(5).all()

        return {
            "statistics": stats,
            "top_authors": [{"name": a.name, "books": a.count} for a in top_authors],
            "top_genres": [{"name": g.name, "books": g.count} for g in top_genres],
            "recent_books": [{"title": b.title, "added": str(b.created_at)} for b in recent_books]
        }

