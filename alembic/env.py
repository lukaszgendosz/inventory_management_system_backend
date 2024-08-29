from alembic import context

from app.database import Database
from app.configs.config import settings
from app.models import Base
from app.configs.containers import Application
from dependency_injector.wiring import inject, Provide

target_metadata = Base.metadata


def run_migrations_online():
    db = Database(settings.DATABASE_URI)
    with db._engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()