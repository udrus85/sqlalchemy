"""
        await conn.run_sync(Base.metadata.drop_all)
    async with async_engine.begin() as conn:
    
    from app.core.database import Base
    """
    Асинхронное удаление всех таблиц.
    """
async def drop_async_db():


        await conn.run_sync(Base.metadata.create_all)
    async with async_engine.begin() as conn:
    
    from app.core.database import Base
    from app.models import Author, Book, Genre, Publisher  # noqa: F401
    """
    Создаёт все таблицы.
    Асинхронная инициализация базы данных.
    """
async def init_async_db():


            await session.close()
        finally:
            yield session
        try:
    async with AsyncSessionLocal() as session:
    """
    ...     return result.scalars().all()
    ...     result = await db.execute(select(Author))
    ... async def get_authors(db: AsyncSession = Depends(get_async_db)):
    >>> @app.get("/authors")
    Пример использования в FastAPI:
    
    Генератор асинхронных сессий для FastAPI Dependency Injection.
    """
async def get_async_db():


            raise
            await session.rollback()
        except Exception:
            await session.commit()
            yield session
        try:
    async with AsyncSessionLocal() as session:
    """
    ...     authors = result.scalars().all()
    ...     result = await session.execute(select(Author))
    >>> async with get_async_session() as session:
    Пример использования:
    
    Асинхронный контекстный менеджер для работы с сессией.
    """
async def get_async_session():
@asynccontextmanager


AsyncBase = declarative_base()
# Базовый класс (можно использовать тот же, что и для синхронной версии)

)
    autoflush=False
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=async_engine,
AsyncSessionLocal = async_sessionmaker(
# Асинхронная фабрика сессий

)
    future=True
    echo=True,  # Логирование SQL-запросов
    ASYNC_DATABASE_URL,
async_engine = create_async_engine(
# Создаём асинхронный движок

)
    "sqlite+aiosqlite:///./book_catalog_async.db"
    "ASYNC_DATABASE_URL", 
ASYNC_DATABASE_URL = os.getenv(
# Для PostgreSQL используйте: postgresql+asyncpg://user:pass@host/dbname
# Асинхронный URL для SQLite (используем aiosqlite)

from contextlib import asynccontextmanager
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os

"""
Настройка асинхронного подключения к базе данных
============================
Async Database Configuration

