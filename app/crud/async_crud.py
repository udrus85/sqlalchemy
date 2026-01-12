"""
Async CRUD Operations
=====================
Асинхронные CRUD операции для демонстрации async SQLAlchemy
"""

from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class AsyncBaseCRUD(Generic[ModelType]):
    """
    Асинхронный базовый класс с CRUD операциями.
    
    Демонстрирует использование SQLAlchemy с async/await.
    """
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def create(self, db: AsyncSession, **kwargs) -> ModelType:
        """
        Асинхронное создание записи.
        
        Args:
            db: Асинхронная сессия
            **kwargs: Поля объекта
            
        Returns:
            Созданный объект
        """
        db_obj = self.model(**kwargs)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Асинхронное получение записи по ID.
        
        Args:
            db: Асинхронная сессия
            id: ID записи
            
        Returns:
            Объект или None
        """
        result = await db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ModelType]:
        """
        Асинхронное получение списка записей.
        
        Args:
            db: Асинхронная сессия
            skip: Пропустить записей
            limit: Лимит записей
            
        Returns:
            Список объектов
        """
        result = await db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def update(
        self, 
        db: AsyncSession, 
        *, 
        id: int, 
        **kwargs
    ) -> Optional[ModelType]:
        """
        Асинхронное обновление записи.
        
        Args:
            db: Асинхронная сессия
            id: ID записи
            **kwargs: Поля для обновления
            
        Returns:
            Обновлённый объект или None
        """
        db_obj = await self.get(db, id)
        if db_obj is None:
            return None
        
        for field, value in kwargs.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, *, id: int) -> bool:
        """
        Асинхронное удаление записи.
        
        Args:
            db: Асинхронная сессия
            id: ID записи
            
        Returns:
            True если удалено, False если не найдено
        """
        db_obj = await self.get(db, id)
        if db_obj is None:
            return False
        
        await db.delete(db_obj)
        await db.commit()
        return True
    
    async def count(self, db: AsyncSession) -> int:
        """
        Асинхронный подсчёт записей.
        
        Returns:
            Количество записей
        """
        result = await db.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar() or 0


# ==================== Специализированные асинхронные CRUD ====================

from app.models.author import Author
from app.models.book import Book
from app.models.genre import Genre
from app.models.publisher import Publisher


class AsyncAuthorCRUD(AsyncBaseCRUD[Author]):
    """Асинхронный CRUD для авторов."""
    
    def __init__(self):
        super().__init__(Author)
    
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Author]:
        """Найти автора по имени."""
        result = await db.execute(
            select(Author).where(Author.name == name)
        )
        return result.scalar_one_or_none()
    
    async def search_by_name(self, db: AsyncSession, name: str) -> List[Author]:
        """Поиск авторов по части имени."""
        result = await db.execute(
            select(Author).where(Author.name.ilike(f"%{name}%"))
        )
        return result.scalars().all()
    
    async def get_with_books(self, db: AsyncSession, author_id: int) -> Optional[Author]:
        """Получить автора с книгами (eager loading)."""
        result = await db.execute(
            select(Author)
            .options(selectinload(Author.books))
            .where(Author.id == author_id)
        )
        return result.scalar_one_or_none()


class AsyncBookCRUD(AsyncBaseCRUD[Book]):
    """Асинхронный CRUD для книг."""
    
    def __init__(self):
        super().__init__(Book)
    
    async def get_by_isbn(self, db: AsyncSession, isbn: str) -> Optional[Book]:
        """Найти книгу по ISBN."""
        result = await db.execute(
            select(Book).where(Book.isbn == isbn)
        )
        return result.scalar_one_or_none()
    
    async def get_by_author(
        self, 
        db: AsyncSession, 
        author_id: int
    ) -> List[Book]:
        """Получить все книги автора."""
        result = await db.execute(
            select(Book).where(Book.author_id == author_id)
        )
        return result.scalars().all()
    
    async def get_with_relations(
        self, 
        db: AsyncSession, 
        book_id: int
    ) -> Optional[Book]:
        """Получить книгу со всеми связями."""
        result = await db.execute(
            select(Book)
            .options(
                selectinload(Book.author),
                selectinload(Book.publisher),
                selectinload(Book.genres)
            )
            .where(Book.id == book_id)
        )
        return result.scalar_one_or_none()
    
    async def add_genre(
        self, 
        db: AsyncSession, 
        book_id: int, 
        genre_id: int
    ) -> Optional[Book]:
        """Добавить жанр к книге."""
        book = await self.get_with_relations(db, book_id)
        if not book:
            return None
        
        genre_result = await db.execute(
            select(Genre).where(Genre.id == genre_id)
        )
        genre = genre_result.scalar_one_or_none()
        
        if genre and genre not in book.genres:
            book.genres.append(genre)
            await db.commit()
            await db.refresh(book)
        
        return book


class AsyncGenreCRUD(AsyncBaseCRUD[Genre]):
    """Асинхронный CRUD для жанров."""
    
    def __init__(self):
        super().__init__(Genre)
    
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Genre]:
        """Найти жанр по названию."""
        result = await db.execute(
            select(Genre).where(Genre.name == name)
        )
        return result.scalar_one_or_none()
    
    async def get_or_create(
        self, 
        db: AsyncSession, 
        name: str, 
        description: str = None
    ) -> Genre:
        """Получить или создать жанр."""
        genre = await self.get_by_name(db, name)
        if genre:
            return genre
        return await self.create(db, name=name, description=description)


class AsyncPublisherCRUD(AsyncBaseCRUD[Publisher]):
    """Асинхронный CRUD для издательств."""
    
    def __init__(self):
        super().__init__(Publisher)
    
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Publisher]:
        """Найти издательство по названию."""
        result = await db.execute(
            select(Publisher).where(Publisher.name == name)
        )
        return result.scalar_one_or_none()


# Синглтоны для удобства
async_author_crud = AsyncAuthorCRUD()
async_book_crud = AsyncBookCRUD()
async_genre_crud = AsyncGenreCRUD()
async_publisher_crud = AsyncPublisherCRUD()

