# 📚 SQLAlchemy Portfolio — Book Catalog

Демонстрационный проект для портфолио, показывающий навыки работы с **SQLAlchemy ORM**.

## 🎯 Что демонстрирует этот проект

- ✅ Модели с разными типами связей (One-to-Many, Many-to-Many)
- ✅ CRUD операции
- ✅ Миграции с Alembic
- ✅ Продвинутые запросы (JOIN, GROUP BY, подзапросы)
- ✅ Асинхронная работа с базой данных
- ✅ Чистая структура проекта

## 📂 Структура проекта

```
sqlalchemy-portfolio/
├── app/
│   ├── core/           # Конфигурация БД
│   ├── models/         # SQLAlchemy модели
│   ├── crud/           # CRUD операции
│   ├── queries/        # Продвинутые запросы
│   └── schemas/        # Pydantic схемы
├── alembic/            # Миграции
├── tests/              # Тесты
├── examples/           # Примеры использования
└── requirements.txt
```

## 🗃️ Модели данных

### Предметная область: Книжный каталог

- **Author** — авторы книг
- **Book** — книги
- **Genre** — жанры (Many-to-Many с Book)
- **Publisher** — издательства

### Диаграмма связей

```
Publisher (1) ──── (N) Book (N) ──── (N) Genre
                        │
                        │
Author (1) ────────── (N)
```

## 🚀 Установка

```bash
# Клонировать репозиторий
git clone https://github.com/YOUR_USERNAME/sqlalchemy-portfolio.git
cd sqlalchemy-portfolio

# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
alembic upgrade head
```

## 📝 Примеры использования

```python
from app.core.database import get_session
from app.crud.author import AuthorCRUD

# Создание автора
with get_session() as session:
    author = AuthorCRUD.create(
        session,
        name="Фёдор Достоевский",
        bio="Русский писатель и мыслитель"
    )
    print(f"Создан автор: {author.name}")
```

## 🧪 Тестирование

```bash
pytest tests/ -v
```

## 📄 Лицензия

MIT License

