"""
Example: Async Operations
=========================
Пример асинхронных операций с SQLAlchemy
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date
from app.core.database_async import get_async_session, init_async_db
from app.crud.async_crud import (
    async_author_crud,
    async_book_crud,
    async_genre_crud,
    async_publisher_crud
)


async def run_example():
    """Демонстрация асинхронных CRUD операций."""

    print("=" * 60)
    print("📚 SQLAlchemy Portfolio - Асинхронные операции")
    print("=" * 60)

    # Инициализируем базу данных
    await init_async_db()
    print("\n✅ Асинхронная база данных инициализирована\n")

    async with get_async_session() as db:
        # ==================== CREATE ====================
        print("📝 ASYNC CREATE")
        print("-" * 40)

        # Создаём издательство
        publisher = await async_publisher_crud.create(
            db,
            name="Питер",
            address="Санкт-Петербург",
            website="https://piter.com"
        )
        print(f"  ✓ Издательство: {publisher.name}")

        # Создаём жанры
        genre1 = await async_genre_crud.create(
            db, name="Программирование", description="Книги о программировании"
        )
        genre2 = await async_genre_crud.create(
            db, name="Python", description="Книги о Python"
        )
        print(f"  ✓ Жанры: {genre1.name}, {genre2.name}")

        # Создаём автора
        author = await async_author_crud.create(
            db,
            name="Марк Лутц",
            bio="Автор книг по Python",
            country="США"
        )
        print(f"  ✓ Автор: {author.name}")

        # Создаём книгу
        book = await async_book_crud.create(
            db,
            title="Изучаем Python",
            isbn="978-5-4461-0000-0",
            description="Полное руководство по Python",
            pages=1500,
            price=2500.0,
            author_id=author.id,
            publisher_id=publisher.id,
            language="Russian"
        )
        print(f"  ✓ Книга: '{book.title}'")

        # Добавляем жанры
        await async_book_crud.add_genre(db, book.id, genre1.id)
        await async_book_crud.add_genre(db, book.id, genre2.id)
        print("  ✓ Жанры добавлены к книге\n")

        # ==================== READ ====================
        print("📖 ASYNC READ")
        print("-" * 40)

        # Получаем книгу
        fetched_book = await async_book_crud.get(db, book.id)
        print(f"  ✓ Книга по ID: {fetched_book.title}")

        # Получаем книгу по ISBN
        book_by_isbn = await async_book_crud.get_by_isbn(db, "978-5-4461-0000-0")
        print(f"  ✓ Книга по ISBN: {book_by_isbn.title}")

        # Получаем автора с книгами
        author_with_books = await async_author_crud.get_with_books(db, author.id)
        print(f"  ✓ Автор {author_with_books.name} имеет {len(author_with_books.books)} книг(и)")

        # Получаем книгу со связями
        book_full = await async_book_crud.get_with_relations(db, book.id)
        print(f"  ✓ Книга '{book_full.title}':")
        print(f"      Автор: {book_full.author.name}")
        print(f"      Издательство: {book_full.publisher.name}")
        print(f"      Жанры: {', '.join(g.name for g in book_full.genres)}\n")

        # ==================== UPDATE ====================
        print("✏️ ASYNC UPDATE")
        print("-" * 40)

        updated_book = await async_book_crud.update(db, id=book.id, price=2299.0)
        print(f"  ✓ Новая цена: {updated_book.price} руб.\n")

        # ==================== PARALLEL OPERATIONS ====================
        print("⚡ Параллельные асинхронные операции")
        print("-" * 40)

        # Создаём несколько авторов параллельно
        tasks = [
            async_author_crud.create(db, name=f"Автор {i}", country="Россия")
            for i in range(1, 4)
        ]

        # Ждём завершения всех задач
        # Примечание: в реальном приложении лучше использовать отдельные сессии
        # для параллельных операций
        for task in tasks:
            new_author = await task
            print(f"  ✓ Создан: {new_author.name}")

        # ==================== COUNT ====================
        print("\n📊 Статистика")
        print("-" * 40)

        authors_count = await async_author_crud.count(db)
        books_count = await async_book_crud.count(db)
        genres_count = await async_genre_crud.count(db)

        print(f"  • Авторов: {authors_count}")
        print(f"  • Книг: {books_count}")
        print(f"  • Жанров: {genres_count}")

    print("\n" + "=" * 60)
    print("✅ Асинхронный пример успешно выполнен!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_example())

