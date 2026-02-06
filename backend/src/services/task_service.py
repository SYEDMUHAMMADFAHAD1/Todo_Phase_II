import uuid
from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.task import Task, TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_create: TaskCreate, user_id: str) -> Task:
        # Create task directly with all required fields
        from datetime import datetime as dt
        now = dt.utcnow()

        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            is_completed=task_create.is_completed,
            user_id=user_id,  # Changed from owner_id to user_id to match the database column
            created_at=now,
            updated_at=now
        )
        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)
        return db_task

    async def get_tasks(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> Sequence[Task]:
        statement = (
            select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_task(self, task_id: str | uuid.UUID, user_id: str) -> Task | None:
        # Convert string to UUID if needed for proper comparison
        task_id_for_query = str(task_id) if isinstance(task_id, uuid.UUID) else task_id
        
        statement = select(Task).where(Task.id == task_id_for_query, Task.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def update_task(
        self, task_id: str | uuid.UUID, user_id: str, task_update: TaskUpdate
    ) -> Task | None:
        db_task = await self.get_task(task_id, user_id)
        if not db_task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        db_task.updated_at = datetime.utcnow()

        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)
        return db_task

    async def delete_task(self, task_id: str | uuid.UUID, user_id: str) -> bool:
        # Convert to string for database comparison since the DB stores IDs as strings
        task_id_for_query = str(task_id) if isinstance(task_id, uuid.UUID) else task_id

        # Use a direct delete statement instead of fetch-then-delete
        statement = select(Task).where(Task.id == task_id_for_query, Task.user_id == user_id)
        result = await self.session.execute(statement)
        db_task = result.scalar_one_or_none()
        
        if not db_task:
            return False

        # Now delete the task
        delete_statement = (
            delete(Task)
            .where(Task.id == task_id_for_query, Task.user_id == user_id)
            .execution_options(synchronize_session=False)  # Skip ORM-level synchronization
        )
        await self.session.execute(delete_statement)
        await self.session.commit()
        
        return True

    async def mark_complete(self, task_id: str | uuid.UUID, user_id: str) -> Task | None:
        return await self.update_task(task_id, user_id, TaskUpdate(is_completed=True))
