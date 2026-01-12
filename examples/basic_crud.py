"""
    run_example()
if __name__ == "__main__":


    print("=" * 60)
    print("✅ Пример успешно выполнен!")
    print("\n" + "=" * 60)
    
        print(f"  • Всего издательств: {publisher_crud.count(db)}")
        print(f"  • Всего жанров: {genre_crud.count(db)}")
        print(f"  • Всего книг: {book_crud.count(db)}")
        print(f"  • Всего авторов: {author_crud.count(db)}")
        print("-" * 40)
        print("\n📊 Статистика")
        # Статистика
        
        print(f"  ✓ Жанры после удаления: {', '.join(book_updated.genre_names)}")
        book_updated = book_crud.get_with_relations(db, book1.id)
        book_crud.remove_genre_from_book(db, book1.id, genre3.id)
        # Удаляем жанр из книги
        
        print("-" * 40)
        print("🗑️ DELETE - Удаление записей")
        # ==================== DELETE ====================
        
        print(f"  ✓ Новая цена книги '{updated_book.title}': {updated_book.price} руб.\n")
        updated_book = book_crud.update(db, id=book1.id, price=649.0)
        # Обновляем цену книги
        
        print("-" * 40)
        print("✏️ UPDATE - Обновление записей")
        # ==================== UPDATE ====================
        
        print(f"  ✓ Найдено книг по запросу 'Преступление': {len(search_results)}\n")
        search_results = book_crud.search_by_title(db, "Преступление")
        # Поиск книг
        
        print(f"      Жанры: {', '.join(book_full.genre_names)}")
        print(f"      Издательство: {book_full.publisher.name}")
        print(f"      Автор: {book_full.author.name}")
        print(f"  ✓ Книга '{book_full.title}':")
        book_full = book_crud.get_with_relations(db, book1.id)
        # Получаем книгу со всеми связями
        
        print(f"  ✓ Автор {author_with_books.name} имеет {len(author_with_books.books)} книг(и)")
        author_with_books = author_crud.get_with_books(db, author.id)
        # Получаем автора с книгами
        
        print(f"  ✓ Книга по ISBN: {book_by_isbn.title}")
        book_by_isbn = book_crud.get_by_isbn(db, "978-5-04-098001-1")
        # Получаем книгу по ISBN
        
        print(f"  ✓ Книга по ID: {fetched_book.title}")
        fetched_book = book_crud.get(db, book1.id)
        # Получаем книгу по ID
        
        print("-" * 40)
        print("📖 READ - Чтение записей")
        # ==================== READ ====================
        
        print("  ✓ Жанры добавлены к книгам\n")
        book_crud.add_genre_to_book(db, book2.id, genre2.id)
        book_crud.add_genre_to_book(db, book2.id, genre1.id)
        
        book_crud.add_genre_to_book(db, book1.id, genre3.id)
        book_crud.add_genre_to_book(db, book1.id, genre2.id)
        book_crud.add_genre_to_book(db, book1.id, genre1.id)
        # Добавляем жанры к книгам (Many-to-Many)
        
        print(f"  ✓ Книги: '{book1.title}', '{book2.title}'")
        )
            publisher_id=publisher.id
            author_id=author.id,
            publication_date=date(1880, 1, 1),
            price=799.0,
            pages=928,
            description="Последний роман Достоевского",
            isbn="978-5-04-098001-2",
            title="Братья Карамазовы",
            db,
        book2 = book_crud.create(
        
        )
            publisher_id=publisher.id
            author_id=author.id,
            publication_date=date(1866, 1, 1),
            price=599.0,
            pages=672,
            description="Роман о студенте Раскольникове",
            isbn="978-5-04-098001-1",
            title="Преступление и наказание",
            db,
        book1 = book_crud.create(
        # Создаём книги
        
        print(f"  ✓ Автор: {author.name}")
        )
            country="Россия"
            birth_date=date(1821, 11, 11),
            bio="Великий русский писатель и мыслитель",
            name="Фёдор Достоевский",
            db,
        author = author_crud.create(
        # Создаём автора
        
        print(f"  ✓ Жанры: {genre1.name}, {genre2.name}, {genre3.name}")
        genre3 = genre_crud.create(db, name="Психология", description="Психологические произведения")
        genre2 = genre_crud.create(db, name="Классика", description="Классическая литература")
        genre1 = genre_crud.create(db, name="Роман", description="Художественная проза")
        # Создаём жанры
        
        print(f"  ✓ Издательство: {publisher.name}")
        )
            website="https://eksmo.ru"
            address="Москва, ул. Пушкина",
            name="Эксмо",
            db,
        publisher = publisher_crud.create(
        # Создаём издательство
        
        print("-" * 40)
        print("📝 CREATE - Создание записей")
        # ==================== CREATE ====================
    with get_session() as db:
    
    print("\n✅ База данных инициализирована\n")
    init_db()
    
    print("=" * 60)
    print("📚 SQLAlchemy Portfolio - Пример CRUD операций")
    print("=" * 60)
    # Инициализируем базу данных
    
    """Демонстрация базовых CRUD операций."""
def run_example():


from app.crud import author_crud, book_crud, genre_crud, publisher_crud
from app.core.database import get_session, init_db
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent))
# Добавляем корень проекта в PYTHONPATH

from pathlib import Path
import sys

"""
Пример базовых CRUD операций с книжным каталогом
==============================
Example: Basic CRUD Operations

