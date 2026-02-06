#!/usr/bin/env python3

import asyncio
import sys
import traceback
from datetime import datetime
from uuid import uuid4

# Setup path
sys.path.insert(0, '/c/hackthone2_clone/Todo_App')

from backend.src.core.db import get_session, engine, init_db
from backend.src.models.task import Task, User
from sqlmodel import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

async def debug():
    # Initialize database
    await init_db()
    print("[OK] Database initialized")

    # Get a session using the generator
    session = None
    async for s in get_session():
        session = s
        break

        # Create a test user
        test_user = User(
            id=str(uuid4()),
            email="debuguser@example.com",
            name="Debug User",
            password="hashedpass"
        )
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)
        print(f"[OK] User created: {test_user.id}")

        # Try to create a task
        try:
            test_task = Task(
                id=str(uuid4()),
                title="Debug Task",
                description="This is a debug task",
                is_completed=False,
                user_id=test_user.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(test_task)
            await session.commit()
            await session.refresh(test_task)
            print(f"[OK] Task created: {test_task.id}")

            # Verify we can read it back
            result = await session.execute(select(Task).where(Task.id == test_task.id))
            retrieved_task = result.scalars().first()
            print(f"[OK] Task retrieved: {retrieved_task.title}")

        except Exception as e:
            print(f"[ERROR] Failed to create task: {e}")
            traceback.print_exc()
    else:
        print("[ERROR] Could not get database session")

if __name__ == "__main__":
    asyncio.run(debug())
