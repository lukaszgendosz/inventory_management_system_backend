from alembic import context

from app.database import engine
from app.models.base import Base

target_metadata = Base.metadata

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # connectable = create_async_engine(config.DATABASE_URI, future=True)

    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()