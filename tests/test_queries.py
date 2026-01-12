"""
Test Advanced Queries
=====================
Тесты для продвинутых запросов
"""

import pytest
from datetime import date


@pytest.fixture
def populated_db(db):
    """Фикстура с заполненной базой данных."""
    from app.crud import author_crud, book_crud, genre_crud, publisher_crud

    # Издательства
    pub1 = publisher_crud.create(db, name="Издательство 1")
    pub2 = publisher_crud.create(db, name="Издательство 2")

    # Жанры
    novel = genre_crud.create(db, name="Роман")
    detective = genre_crud.create(db, name="Детектив")

    # Авторы и книги
    author1 = author_crud.create(db, name="Автор 1", country="Россия")
    author2 = author_crud.create(db, name="Автор 2", country="США")
    author3 = author_crud.create(db, name="Автор без книг", country="Россия")

    # Книги для author1
    book1 = book_crud.create(
        db, title="Книга 1", price=500, pages=300,
        author_id=author1.id, publisher_id=pub1.id, language="Russian"
    )
    book2 = book_crud.create(
        db, title="Книга 2", price=800, pages=400,
        author_id=author1.id, publisher_id=pub1.id, language="Russian"
    )

    # Книги для author2
    book3 = book_crud.create(
        db, title="Книга 3", price=1200, pages=500,
        author_id=author2.id, publisher_id=pub2.id, language="English"
    )

    # Добавляем жанры
    book_crud.add_genre_to_book(db, book1.id, novel.id)
    book_crud.add_genre_to_book(db, book2.id, novel.id)
    book_crud.add_genre_to_book(db, book3.id, detective.id)

    return {
        "authors": [author1, author2, author3],
        "books": [book1, book2, book3],
        "genres": [novel, detective],
        "publishers": [pub1, pub2]
    }


class TestAggregateQueries:
    """Тесты для агрегатных запросов."""

    def test_library_statistics(self, db, populated_db):
        """Тест общей статистики."""
        from app.queries.advanced import AdvancedQueries

        stats = AdvancedQueries.get_library_statistics(db)

        assert stats["total_books"] == 3
        assert stats["total_authors"] == 2  # Только авторы с книгами
        assert stats["avg_price"] > 0

    def test_books_count_by_language(self, db, populated_db):
        """Тест подсчёта книг по языкам."""
        from app.queries.advanced import AdvancedQueries

        result = AdvancedQueries.get_books_count_by_language(db)

        languages = dict(result)
        assert languages.get("Russian", 0) == 2
        assert languages.get("English", 0) == 1


class TestGroupByQueries:
    """Тесты для GROUP BY запросов."""

    def test_prolific_authors(self, db, populated_db):
        """Тест плодовитых авторов."""
        from app.queries.advanced import AdvancedQueries

        result = AdvancedQueries.get_prolific_authors(db, min_books=2)

        assert len(result) == 1
        assert result[0][0] == "Автор 1"
        assert result[0][1] == 2

    def test_genre_statistics(self, db, populated_db):
        """Тест статистики по жанрам."""
        from app.queries.advanced import AdvancedQueries

        result = AdvancedQueries.get_genre_statistics(db)

        assert len(result) == 2

        # Роман должен иметь 2 книги
        novel_stats = next((g for g in result if g["genre"] == "Роман"), None)
        assert novel_stats is not None
        assert novel_stats["book_count"] == 2


class TestJoinQueries:
    """Тесты для JOIN запросов."""

    def test_authors_without_books(self, db, populated_db):
        """Тест авторов без книг."""
        from app.queries.advanced import AdvancedQueries

        result = AdvancedQueries.get_authors_without_books(db)

        assert len(result) == 1
        assert result[0].name == "Автор без книг"

    def test_books_with_author_and_publisher(self, db, populated_db):
        """Тест книг с авторами и издательствами."""
        from app.queries.advanced import AdvancedQueries

        result = AdvancedQueries.get_books_with_author_and_publisher(db)

        assert len(result) == 3
        assert all(b["author"] is not None for b in result)


class TestSubqueries:
    """Тесты для подзапросов."""

    def test_books_above_average_price(self, db, populated_db):
        """Тест книг дороже средней цены."""
        from app.queries.advanced import AdvancedQueries

        result = AdvancedQueries.get_books_above_average_price(db)

        # Средняя цена = (500+800+1200)/3 ≈ 833
        # Книга 3 (1200) дороже средней
        assert len(result) >= 1
        assert all(b.price > 800 for b in result)


class TestCaseQueries:
    """Тесты для CASE WHEN запросов."""

    def test_books_with_price_category(self, db, populated_db):
        """Тест категорий цен."""
        from app.queries.advanced import AdvancedQueries

        result = AdvancedQueries.get_books_with_price_category(db)

        assert len(result) == 3

        # Проверяем категории
        categories = {b["title"]: b["category"] for b in result}
        assert categories["Книга 1"] == "Средняя"  # 500
        assert categories["Книга 2"] == "Дорогая"  # 800

    def test_author_rating_by_books(self, db, populated_db):
        """Тест рейтинга авторов."""
        from app.queries.advanced import AdvancedQueries

        result = AdvancedQueries.get_author_rating_by_books(db)

        ratings = {r["author"]: r["rating"] for r in result}

        # Автор 1 с 2 книгами должен быть "Начинающий"
        assert ratings["Автор 1"] == "Начинающий"

        # Автор без книг должен быть "Дебютант"
        assert ratings["Автор без книг"] == "Дебютант"


class TestPaginationQueries:
    """Тесты для пагинации."""

    def test_sorted_books_asc(self, db, populated_db):
        """Тест сортировки по возрастанию."""
        from app.queries.advanced import AdvancedQueries

        result = AdvancedQueries.get_books_sorted(
            db, sort_by="price", order="asc", limit=10
        )

        prices = [b.price for b in result]
        assert prices == sorted(prices)

    def test_sorted_books_desc(self, db, populated_db):
        """Тест сортировки по убыванию."""
        from app.queries.advanced import AdvancedQueries

        result = AdvancedQueries.get_books_sorted(
            db, sort_by="price", order="desc", limit=10
        )

        prices = [b.price for b in result]
        assert prices == sorted(prices, reverse=True)

    def test_pagination(self, db, populated_db):
        """Тест пагинации."""
        from app.queries.advanced import AdvancedQueries

        # Первая страница
        page1 = AdvancedQueries.get_books_sorted(db, skip=0, limit=2)
        # Вторая страница
        page2 = AdvancedQueries.get_books_sorted(db, skip=2, limit=2)

        assert len(page1) == 2
        assert len(page2) == 1

        # Убеждаемся, что страницы не пересекаются
        ids_page1 = {b.id for b in page1}
        ids_page2 = {b.id for b in page2}
        assert ids_page1.isdisjoint(ids_page2)

