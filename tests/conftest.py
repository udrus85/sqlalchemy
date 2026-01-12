"""
    )
        language="Russian"
        publisher_id=sample_publisher.id,
        author_id=sample_author.id,
        publication_date=date(2023, 1, 1),
        price=500.0,
        pages=300,
        description="Описание тестовой книги",
        isbn="978-5-00000-000-0",
        title="Тестовая Книга",
        db,
    return book_crud.create(
    
    from datetime import date
    from app.crud import book_crud
    """Фикстура для создания тестовой книги."""
def sample_book(db, sample_author, sample_publisher):
@pytest.fixture


    )
        description="Описание тестового жанра"
        name="Тестовый Жанр",
        db,
    return genre_crud.create(
    
    from app.crud import genre_crud
    """Фикстура для создания тестового жанра."""
def sample_genre(db):
@pytest.fixture


    )
        website="https://test.com"
        address="Москва",
        name="Тестовое Издательство",
        db,
    return publisher_crud.create(
    
    from app.crud import publisher_crud
    """Фикстура для создания тестового издательства."""
def sample_publisher(db):
@pytest.fixture


    )
        country="Россия"
        birth_date=date(1990, 1, 1),
        bio="Биография тестового автора",
        name="Тестовый Автор",
        db,
    return author_crud.create(
    
    from datetime import date
    from app.crud import author_crud
    """Фикстура для создания тестового автора."""
def sample_author(db):
@pytest.fixture


        Base.metadata.drop_all(bind=test_engine)
        # Удаляем таблицы после теста
        session.close()
    finally:
        yield session
    try:
    
    session = TestSessionLocal()
    # Создаём сессию
    
    Base.metadata.create_all(bind=test_engine)
    # Создаём таблицы
    
    from app.models import Author, Book, Genre, Publisher  # noqa: F401
    # Импортируем модели, чтобы они зарегистрировались
    """
    Создаёт все таблицы перед тестом и удаляет после.

    Фикстура для создания тестовой сессии базы данных.
    """
def db():
@pytest.fixture(scope="function")


)
    bind=test_engine
    autoflush=False,
    autocommit=False,
TestSessionLocal = sessionmaker(

)
    connect_args={"check_same_thread": False}
    TEST_DATABASE_URL,
test_engine = create_engine(

TEST_DATABASE_URL = "sqlite:///:memory:"
# Тестовая база данных в памяти


from app.core.database import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
# Добавляем корень проекта в PYTHONPATH

from pathlib import Path
import sys

"""
Настройка pytest для тестов
===================
Tests Configuration

