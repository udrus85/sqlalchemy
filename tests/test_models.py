"""
Test Models
===========
Тесты для моделей SQLAlchemy
"""

from datetime import date
import pytest


class TestAuthorModel:
    """Тесты для модели Author."""

    def test_author_creation(self, db, sample_author):
        """Тест создания автора."""
        assert sample_author.id is not None
        assert sample_author.name == "Тестовый Автор"
        assert sample_author.country == "Россия"

    def test_author_repr(self, sample_author):
        """Тест строкового представления."""
        assert "Тестовый Автор" in repr(sample_author)

    def test_author_books_count(self, sample_author):
        """Тест подсчёта книг автора."""
        assert sample_author.books_count == 0


class TestBookModel:
    """Тесты для модели Book."""

    def test_book_creation(self, sample_book):
        """Тест создания книги."""
        assert sample_book.id is not None
        assert sample_book.title == "Тестовая Книга"
        assert sample_book.isbn == "978-5-00000-000-0"
        assert sample_book.price == 500.0

    def test_book_author_relation(self, sample_book, sample_author):
        """Тест связи книги с автором."""
        assert sample_book.author_id == sample_author.id
        assert sample_book.author.name == sample_author.name

    def test_book_publisher_relation(self, sample_book, sample_publisher):
        """Тест связи книги с издательством."""
        assert sample_book.publisher_id == sample_publisher.id
        assert sample_book.publisher.name == sample_publisher.name

    def test_book_genre_names_empty(self, sample_book):
        """Тест пустого списка жанров."""
        assert sample_book.genre_names == []


class TestGenreModel:
    """Тесты для модели Genre."""

    def test_genre_creation(self, sample_genre):
        """Тест создания жанра."""
        assert sample_genre.id is not None
        assert sample_genre.name == "Тестовый Жанр"


class TestPublisherModel:
    """Тесты для модели Publisher."""

    def test_publisher_creation(self, sample_publisher):
        """Тест создания издательства."""
        assert sample_publisher.id is not None
        assert sample_publisher.name == "Тестовое Издательство"


class TestManyToManyRelation:
    """Тесты для Many-to-Many связей."""

    def test_add_genre_to_book(self, db, sample_book, sample_genre):
        """Тест добавления жанра к книге."""
        from app.crud import book_crud

        book = book_crud.add_genre_to_book(db, sample_book.id, sample_genre.id)

        assert sample_genre in book.genres
        assert sample_genre.name in book.genre_names

    def test_multiple_genres(self, db, sample_book):
        """Тест нескольких жанров у книги."""
        from app.crud import genre_crud, book_crud

        genre1 = genre_crud.create(db, name="Жанр 1")
        genre2 = genre_crud.create(db, name="Жанр 2")

        book_crud.add_genre_to_book(db, sample_book.id, genre1.id)
        book_crud.add_genre_to_book(db, sample_book.id, genre2.id)

        book = book_crud.get_with_relations(db, sample_book.id)

        assert len(book.genres) == 2
        assert "Жанр 1" in book.genre_names
        assert "Жанр 2" in book.genre_names

    def test_remove_genre_from_book(self, db, sample_book, sample_genre):
        """Тест удаления жанра из книги."""
        from app.crud import book_crud

        # Сначала добавляем
        book_crud.add_genre_to_book(db, sample_book.id, sample_genre.id)

        # Затем удаляем
        book = book_crud.remove_genre_from_book(db, sample_book.id, sample_genre.id)

        assert sample_genre not in book.genres

