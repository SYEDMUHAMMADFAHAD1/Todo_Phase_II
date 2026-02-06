import asyncio
from backend.src.core.db import engine, init_db
# Import all models to register them with SQLModel
from backend.src.models import User, Task, TaskCreate, TaskRead, TaskUpdate
from sqlmodel import SQLModel

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_db_and_tables())