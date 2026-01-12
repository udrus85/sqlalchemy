"""
Test CRUD Operations
====================
Тесты для CRUD операций
"""

from datetime import date
import pytest


class TestBaseCRUD:
    """Тесты для базовых CRUD операций."""

    def test_create(self, db, sample_author):
        """Тест создания записи."""
        assert sample_author.id is not None
        assert sample_author.created_at is not None

    def test_get_by_id(self, db, sample_author):
        """Тест получения по ID."""
        from app.crud import author_crud

        fetched = author_crud.get(db, sample_author.id)

        assert fetched is not None
        assert fetched.id == sample_author.id
        assert fetched.name == sample_author.name

    def test_get_nonexistent(self, db):
        """Тест получения несуществующей записи."""
        from app.crud import author_crud

        result = author_crud.get(db, 99999)

        assert result is None

    def test_get_multi(self, db):
        """Тест получения нескольких записей."""
        from app.crud import author_crud

        # Создаём несколько авторов
        for i in range(5):
            author_crud.create(db, name=f"Автор {i}")

        # Получаем с пагинацией
        result = author_crud.get_multi(db, skip=1, limit=3)

        assert len(result) == 3

    def test_update(self, db, sample_author):
        """Тест обновления записи."""
        from app.crud import author_crud

        updated = author_crud.update(
            db,
            id=sample_author.id,
            name="Новое Имя",
            country="США"
        )

        assert updated.name == "Новое Имя"
        assert updated.country == "США"

    def test_delete(self, db, sample_author):
        """Тест удаления записи."""
        from app.crud import author_crud

        result = author_crud.delete(db, id=sample_author.id)

        assert result is True
        assert author_crud.get(db, sample_author.id) is None

    def test_delete_nonexistent(self, db):
        """Тест удаления несуществующей записи."""
        from app.crud import author_crud

        result = author_crud.delete(db, id=99999)

        assert result is False

    def test_count(self, db):
        """Тест подсчёта записей."""
        from app.crud import author_crud

        # Создаём авторов
        for i in range(3):
            author_crud.create(db, name=f"Автор {i}")

        count = author_crud.count(db)

        assert count == 3

    def test_exists(self, db, sample_author):
        """Тест проверки существования."""
        from app.crud import author_crud

        assert author_crud.exists(db, sample_author.id) is True
        assert author_crud.exists(db, 99999) is False


class TestAuthorCRUD:
    """Тесты для AuthorCRUD."""

    def test_get_by_name(self, db, sample_author):
        """Тест поиска по имени."""
        from app.crud import author_crud

        result = author_crud.get_by_name(db, "Тестовый Автор")

        assert result is not None
        assert result.id == sample_author.id

    def test_search_by_name(self, db, sample_author):
        """Тест поиска по части имени."""
        from app.crud import author_crud

        results = author_crud.search_by_name(db, "Тестовый")

        assert len(results) >= 1
        assert any(a.id == sample_author.id for a in results)

    def test_get_by_country(self, db, sample_author):
        """Тест поиска по стране."""
        from app.crud import author_crud

        results = author_crud.get_by_country(db, "Россия")

        assert len(results) >= 1

    def test_get_with_books(self, db, sample_book, sample_author):
        """Тест получения автора с книгами."""
        from app.crud import author_crud

        author = author_crud.get_with_books(db, sample_author.id)

        assert len(author.books) == 1
        assert author.books[0].title == sample_book.title


class TestBookCRUD:
    """Тесты для BookCRUD."""

    def test_get_by_isbn(self, db, sample_book):
        """Тест поиска по ISBN."""
        from app.crud import book_crud

        result = book_crud.get_by_isbn(db, "978-5-00000-000-0")

        assert result is not None
        assert result.id == sample_book.id

    def test_search_by_title(self, db, sample_book):
        """Тест поиска по названию."""
        from app.crud import book_crud

        results = book_crud.search_by_title(db, "Тестовая")

        assert len(results) >= 1

    def test_get_by_author(self, db, sample_book, sample_author):
        """Тест получения книг автора."""
        from app.crud import book_crud

        results = book_crud.get_by_author(db, sample_author.id)

        assert len(results) == 1
        assert results[0].id == sample_book.id

    def test_get_by_price_range(self, db, sample_book):
        """Тест фильтрации по цене."""
        from app.crud import book_crud

        results = book_crud.get_by_price_range(db, min_price=400, max_price=600)

        assert len(results) >= 1
        assert all(400 <= b.price <= 600 for b in results)

    def test_advanced_search(self, db, sample_book, sample_author):
        """Тест расширенного поиска."""
        from app.crud import book_crud

        # Поиск по нескольким критериям
        results = book_crud.advanced_search(
            db,
            title="Тестовая",
            min_price=400,
            language="Russian"
        )

        assert len(results) >= 1


class TestGenreCRUD:
    """Тесты для GenreCRUD."""

    def test_get_by_name(self, db, sample_genre):
        """Тест поиска по названию."""
        from app.crud import genre_crud

        result = genre_crud.get_by_name(db, "Тестовый Жанр")

        assert result is not None
        assert result.id == sample_genre.id

    def test_get_or_create_existing(self, db, sample_genre):
        """Тест get_or_create для существующего жанра."""
        from app.crud import genre_crud

        result = genre_crud.get_or_create(db, "Тестовый Жанр")

        assert result.id == sample_genre.id

    def test_get_or_create_new(self, db):
        """Тест get_or_create для нового жанра."""
        from app.crud import genre_crud

        result = genre_crud.get_or_create(db, "Новый Жанр", "Описание")

        assert result.id is not None
        assert result.name == "Новый Жанр"

