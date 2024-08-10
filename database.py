from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import config


engine = create_async_engine(
    config.DATABASE_URI,
    future=True,
    echo=True
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
