"""
Example: Advanced Queries
=========================
Пример продвинутых запросов SQLAlchemy
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date
from app.core.database import get_session, init_db
from app.crud import author_crud, book_crud, genre_crud, publisher_crud
from app.queries.advanced import AdvancedQueries


def setup_test_data(db):
    """Создаём тестовые данные для демонстрации запросов."""

    # Издательства
    eksmo = publisher_crud.create(db, name="Эксмо", address="Москва")
    ast = publisher_crud.create(db, name="АСТ", address="Москва")
    azbuka = publisher_crud.create(db, name="Азбука", address="Санкт-Петербург")

    # Жанры
    novel = genre_crud.create(db, name="Роман")
    detective = genre_crud.create(db, name="Детектив")
    fantasy = genre_crud.create(db, name="Фантастика")
    classic = genre_crud.create(db, name="Классика")
    horror = genre_crud.create(db, name="Ужасы")

    # Авторы и книги
    authors_data = [
        {
            "name": "Фёдор Достоевский",
            "country": "Россия",
            "books": [
                {"title": "Преступление и наказание", "price": 599, "pages": 672, "genres": [novel, classic]},
                {"title": "Братья Карамазовы", "price": 799, "pages": 928, "genres": [novel, classic]},
                {"title": "Идиот", "price": 549, "pages": 640, "genres": [novel, classic]},
            ]
        },
        {
            "name": "Лев Толстой",
            "country": "Россия",
            "books": [
                {"title": "Война и мир", "price": 899, "pages": 1408, "genres": [novel, classic]},
                {"title": "Анна Каренина", "price": 699, "pages": 864, "genres": [novel, classic]},
            ]
        },
        {
            "name": "Агата Кристи",
            "country": "Великобритания",
            "books": [
                {"title": "Убийство в Восточном экспрессе", "price": 399, "pages": 320, "genres": [detective]},
                {"title": "Десять негритят", "price": 349, "pages": 288, "genres": [detective]},
                {"title": "Убийство Роджера Экройда", "price": 379, "pages": 352, "genres": [detective]},
                {"title": "Смерть на Ниле", "price": 419, "pages": 384, "genres": [detective]},
            ]
        },
        {
            "name": "Стивен Кинг",
            "country": "США",
            "books": [
                {"title": "Сияние", "price": 549, "pages": 512, "genres": [horror, novel]},
                {"title": "Оно", "price": 899, "pages": 1184, "genres": [horror]},
                {"title": "Тёмная башня", "price": 649, "pages": 480, "genres": [fantasy, horror]},
            ]
        },
        {
            "name": "Джордж Мартин",
            "country": "США",
            "books": [
                {"title": "Игра престолов", "price": 749, "pages": 720, "genres": [fantasy]},
                {"title": "Битва королей", "price": 799, "pages": 768, "genres": [fantasy]},
            ]
        },
        {
            "name": "Новый Автор",
            "country": "Россия",
            "books": []  # Автор без книг
        }
    ]

    publishers = [eksmo, ast, azbuka]

    for i, author_data in enumerate(authors_data):
        author = author_crud.create(
            db,
            name=author_data["name"],
            country=author_data["country"]
        )

        for j, book_data in enumerate(author_data["books"]):
            book = book_crud.create(
                db,
                title=book_data["title"],
                price=book_data["price"],
                pages=book_data["pages"],
                author_id=author.id,
                publisher_id=publishers[(i + j) % len(publishers)].id,
                language="Russian" if author_data["country"] == "Россия" else "English"
            )

            for genre in book_data["genres"]:
                book_crud.add_genre_to_book(db, book.id, genre.id)

    print("✅ Тестовые данные созданы\n")


def run_example():
    """Демонстрация продвинутых запросов."""

    print("=" * 60)
    print("📚 SQLAlchemy Portfolio - Продвинутые запросы")
    print("=" * 60)

    init_db()

    with get_session() as db:
        # Создаём тестовые данные
        setup_test_data(db)

        # ==================== АГРЕГАТНЫЕ ФУНКЦИИ ====================
        print("📊 Статистика библиотеки (агрегатные функции)")
        print("-" * 40)

        stats = AdvancedQueries.get_library_statistics(db)
        print(f"  • Всего книг: {stats['total_books']}")
        print(f"  • Авторов: {stats['total_authors']}")
        print(f"  • Средняя цена: {stats['avg_price']} руб.")
        print(f"  • Мин. цена: {stats['min_price']} руб.")
        print(f"  • Макс. цена: {stats['max_price']} руб.")
        print(f"  • Всего страниц: {stats['total_pages']}")

        # ==================== GROUP BY ====================
        print("\n📚 Книги по языкам (GROUP BY)")
        print("-" * 40)

        by_language = AdvancedQueries.get_books_count_by_language(db)
        for lang, count in by_language:
            print(f"  • {lang}: {count} книг")

        # ==================== GROUP BY + HAVING ====================
        print("\n✍️ Плодовитые авторы (GROUP BY + HAVING)")
        print("-" * 40)

        prolific = AdvancedQueries.get_prolific_authors(db, min_books=2)
        for name, count in prolific:
            print(f"  • {name}: {count} книг")

        # ==================== СТАТИСТИКА ПО ЖАНРАМ ====================
        print("\n🎭 Статистика по жанрам")
        print("-" * 40)

        genre_stats = AdvancedQueries.get_genre_statistics(db)
        for g in genre_stats:
            print(f"  • {g['genre']}: {g['book_count']} книг, "
                  f"средняя цена: {g['avg_price']} руб.")

        # ==================== LEFT JOIN + IS NULL ====================
        print("\n👤 Авторы без книг (LEFT JOIN + IS NULL)")
        print("-" * 40)

        authors_no_books = AdvancedQueries.get_authors_without_books(db)
        for author in authors_no_books:
            print(f"  • {author.name}")

        # ==================== ПОДЗАПРОСЫ ====================
        print("\n💰 Книги дороже средней цены (подзапрос)")
        print("-" * 40)

        expensive = AdvancedQueries.get_books_above_average_price(db)
        for book in expensive[:5]:  # Первые 5
            print(f"  • {book.title}: {book.price} руб.")

        # ==================== CASE WHEN ====================
        print("\n🏷️ Категории цен книг (CASE WHEN)")
        print("-" * 40)

        categorized = AdvancedQueries.get_books_with_price_category(db)
        for book in categorized[:5]:
            print(f"  • {book['title']}: {book['price']} руб. - {book['category']}")

        # ==================== РЕЙТИНГ АВТОРОВ ====================
        print("\n⭐ Рейтинг авторов (CASE + агрегация)")
        print("-" * 40)

        ratings = AdvancedQueries.get_author_rating_by_books(db)
        for r in ratings:
            print(f"  • {r['author']}: {r['book_count']} книг - {r['rating']}")

        # ==================== ДАШБОРД ====================
        print("\n📈 Данные для дашборда (комплексный запрос)")
        print("-" * 40)

        dashboard = AdvancedQueries.get_dashboard_data(db)
        print("  Топ авторов:")
        for a in dashboard["top_authors"]:
            print(f"    • {a['name']}: {a['books']} книг")
        print("  Топ жанров:")
        for g in dashboard["top_genres"]:
            print(f"    • {g['name']}: {g['books']} книг")

    print("\n" + "=" * 60)
    print("✅ Пример успешно выполнен!")
    print("=" * 60)


if __name__ == "__main__":
    run_example()

