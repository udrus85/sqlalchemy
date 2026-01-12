"""
Database Configuration
======================
Настройка подключения к базе данных SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
import os

# Получаем URL базы данных из переменной окружения или используем SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./book_catalog.db")

# Создаём движок SQLAlchemy
# echo=True для логирования SQL-запросов (полезно для отладки)
engine = create_engine(
    DATABASE_URL,
    echo=True,
    # Для SQLite нужен этот параметр для работы с несколькими потоками
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Базовый класс для всех моделей
Base = declarative_base()


@contextmanager
def get_session():
    """
    Контекстный менеджер для работы с сессией базы данных.

    Пример использования:
    >>> with get_session() as session:
    ...     authors = session.query(Author).all()
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db():
    """
    Генератор сессий для FastAPI Dependency Injection.

    Пример использования в FastAPI:
    >>> @app.get("/authors")
    ... def get_authors(db: Session = Depends(get_db)):
    ...     return db.query(Author).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Инициализация базы данных - создание всех таблиц.
    Используется только для разработки. В продакшене используйте Alembic миграции.
    """
    # Импортируем модели, чтобы они зарегистрировались в Base.metadata
    from app.models import author, book, genre, publisher  # noqa: F401
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Удаление всех таблиц. ОСТОРОЖНО: удаляет все данные!
    Используется только для тестирования.
    """
    Base.metadata.drop_all(bind=engine)

