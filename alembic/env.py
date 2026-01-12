"""
Alembic Environment Configuration
==================================
Настройка окружения для миграций Alembic
"""

import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Добавляем корень проекта в sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Импортируем конфигурацию базы данных и модели
from app.core.database import Base, DATABASE_URL
from app.models import Author, Book, Genre, Publisher  # noqa: F401

# this is the Alembic Config object
config = context.config

# Устанавливаем URL базы данных из нашей конфигурации
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Интерпретируем файл конфигурации логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей для autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    Генерирует SQL-скрипты без подключения к базе данных.
    Полезно для ревью миграций перед применением.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    Подключается к базе данных и применяет миграции.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Включаем сравнение типов колонок
            compare_type=True,
            # Включаем сравнение server defaults
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

