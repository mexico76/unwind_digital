from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from os import environ
from alembic import context

import settings

from data.db import metadata
from data.models import *

"""
Для корректной генерации файлов миграций в alembic/versions необходимо
импортировать все модели приложения в env.py
Использовать где-либо их при этом не обязательно.
Если модель не импортировать, то при генерации файла миграции
она не будет в нём отображена
"""

config = context.config

"""
Т.к напрямую использовать переменные в .ini файле нельзя,
то используется Alembic Config object, через который можно поместить
переменные и изначения в .ini-конфиг файла
Используем его для того, чтобы прокинуть в alembic.ini данные из settings
"""

section = config.config_ini_section
config.set_section_option(section, "DB_USER", settings.DB_USER)
config.set_section_option(section, "DB_PASS", settings.DB_PASS)
config.set_section_option(section, "DB_NAME", settings.DB_NAME)
config.set_section_option(section, "DB_HOST", settings.DB_HOST)

fileConfig(config.config_file_name)

target_metadata = metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

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


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
