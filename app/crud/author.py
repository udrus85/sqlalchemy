"""
Author CRUD
===========
CRUD операции для модели Author
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import BaseCRUD
from app.models.author import Author


class AuthorCRUD(BaseCRUD[Author]):
    """
    CRUD операции для авторов.
    
    Расширяет базовый CRUD специфичными методами для Author.
    """
    
    def __init__(self):
        super().__init__(Author)
    
    def get_by_name(self, db: Session, name: str) -> Optional[Author]:
        """
        Найти автора по имени (точное совпадение).
        
        Args:
            db: Сессия базы данных
            name: Имя автора
            
        Returns:
            Автор или None
        """
        return db.query(Author).filter(Author.name == name).first()
    
    def search_by_name(self, db: Session, name: str) -> List[Author]:
        """
        Поиск авторов по части имени (LIKE).
        
        Args:
            db: Сессия базы данных
            name: Часть имени для поиска
            
        Returns:
            Список авторов
        """
        return db.query(Author).filter(
            Author.name.ilike(f"%{name}%")
        ).all()
    
    def get_by_country(self, db: Session, country: str) -> List[Author]:
        """
        Получить авторов по стране.
        
        Args:
            db: Сессия базы данных
            country: Название страны
            
        Returns:
            Список авторов из указанной страны
        """
        return db.query(Author).filter(Author.country == country).all()
    
    def get_with_books(self, db: Session, author_id: int) -> Optional[Author]:
        """
        Получить автора вместе с его книгами.
        Использует selectinload для оптимизации.
        
        Args:
            db: Сессия базы данных
            author_id: ID автора
            
        Returns:
            Автор с загруженными книгами или None
        """
        from sqlalchemy.orm import selectinload
        return db.query(Author).options(
            selectinload(Author.books)
        ).filter(Author.id == author_id).first()
    
    def get_authors_with_book_count(
        self, 
        db: Session, 
        min_books: int = 0
    ) -> List[tuple]:
        """
        Получить авторов с количеством их книг.
        Демонстрирует GROUP BY и HAVING.
        
        Args:
            db: Сессия базы данных
            min_books: Минимальное количество книг
            
        Returns:
            Список кортежей (author_name, book_count)
        """
        from sqlalchemy import func
        from app.models.book import Book
        
        query = db.query(
            Author.name,
            func.count(Book.id).label("book_count")
        ).outerjoin(Book).group_by(Author.id, Author.name)
        
        if min_books > 0:
            query = query.having(func.count(Book.id) >= min_books)
        
        return query.all()


# Синглтон для удобства использования
author_crud = AuthorCRUD()

