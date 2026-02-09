from collections.abc import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .config import settings
# Import all models so they're registered with SQLModel.metadata before create_all()
from ..models.task import User, Task
from ..models.conversation import Conversation
from ..models.message import Message

# Create Async Engine
# echo=True can be helpful for debugging SQL queries during development
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)


async def init_db() -> None:
    async with engine.begin() as conn:
        # SQLModel.metadata.create_all is usually for development only
        # In production we use Alembic migrations
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


# Alias for compatibility
get_db = get_session
