"""
Tests for task ownership enforcement at the service layer.

These tests verify that TaskService correctly enforces task ownership
by filtering queries with WHERE user_id = authenticated_user_id.

Tests cover:
- get_task() returns None if task belongs to different user
- get_tasks() returns only user's own tasks
- update_task() fails if task belongs to different user
- delete_task() fails if task belongs to different user
- mark_complete() fails if task belongs to different user
- create_task() assigns correct user_id
"""

import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.task import Task, TaskCreate, TaskUpdate
from backend.src.services.task_service import TaskService


@pytest.mark.asyncio
class TestTaskOwnershipFiltering:
    """Test that TaskService filters queries by user_id"""

    async def test_get_task_returns_none_for_different_owner(
        self, test_session: AsyncSession
    ):
        """get_task() should return None if task belongs to different user"""
        service = TaskService(test_session)

        # Create a task for user-a
        task_create = TaskCreate(title="User A Task")
        created_task = await service.create_task(task_create, "user-a")
        assert created_task.user_id == "user-a"

        # Try to get task as user-b
        result = await service.get_task(created_task.id, "user-b")
        assert result is None

        # Verify user-a can still get their task
        result = await service.get_task(created_task.id, "user-a")
        assert result is not None
        assert result.id == created_task.id

    async def test_get_tasks_returns_only_user_tasks(
        self, test_session: AsyncSession
    ):
        """get_tasks() should only return tasks belonging to the querying user"""
        service = TaskService(test_session)

        # Create tasks for user-a (3 tasks)
        for i in range(3):
            task_create = TaskCreate(title=f"User A Task {i+1}")
            await service.create_task(task_create, "user-a")

        # Create tasks for user-b (2 tasks)
        for i in range(2):
            task_create = TaskCreate(title=f"User B Task {i+1}")
            await service.create_task(task_create, "user-b")

        # Get tasks for user-a
        user_a_tasks = await service.get_tasks("user-a")
        assert len(user_a_tasks) == 3
        assert all(t.user_id == "user-a" for t in user_a_tasks)
        assert all("User A Task" in t.title for t in user_a_tasks)

        # Get tasks for user-b
        user_b_tasks = await service.get_tasks("user-b")
        assert len(user_b_tasks) == 2
        assert all(t.user_id == "user-b" for t in user_b_tasks)
        assert all("User B Task" in t.title for t in user_b_tasks)

        # Users should not see each other's tasks
        assert not any(t.user_id == "user-b" for t in user_a_tasks)
        assert not any(t.user_id == "user-a" for t in user_b_tasks)

    async def test_get_tasks_with_pagination(self, test_session: AsyncSession):
        """get_tasks() with skip/limit should only return user's tasks"""
        service = TaskService(test_session)

        # Create 5 tasks for user-a
        for i in range(5):
            task_create = TaskCreate(title=f"User A Task {i+1}")
            await service.create_task(task_create, "user-a")

        # Get tasks with limit 2
        tasks = await service.get_tasks("user-a", skip=0, limit=2)
        assert len(tasks) == 2
        assert all(t.user_id == "user-a" for t in tasks)

        # Get next page
        tasks_page2 = await service.get_tasks("user-a", skip=2, limit=2)
        assert len(tasks_page2) == 2
        assert all(t.user_id == "user-a" for t in tasks_page2)

        # Verify different items
        first_page_ids = {t.id for t in tasks}
        second_page_ids = {t.id for t in tasks_page2}
        assert len(first_page_ids.intersection(second_page_ids)) == 0

    async def test_update_task_fails_for_different_owner(
        self, test_session: AsyncSession
    ):
        """update_task() should return None if task belongs to different user"""
        service = TaskService(test_session)

        # Create a task for user-a
        task_create = TaskCreate(title="Original Title")
        created_task = await service.create_task(task_create, "user-a")

        # Try to update as user-b
        update = TaskUpdate(title="Hacked Title")
        result = await service.update_task(created_task.id, "user-b", update)
        assert result is None

        # Verify task was not updated
        original_task = await service.get_task(created_task.id, "user-a")
        assert original_task.title == "Original Title"

    async def test_update_task_succeeds_for_owner(
        self, test_session: AsyncSession
    ):
        """update_task() should succeed if task belongs to the user"""
        service = TaskService(test_session)

        # Create a task for user-a
        task_create = TaskCreate(title="Original Title")
        created_task = await service.create_task(task_create, "user-a")

        # Update as user-a
        update = TaskUpdate(title="Updated Title")
        result = await service.update_task(created_task.id, "user-a", update)
        assert result is not None
        assert result.title == "Updated Title"

        # Verify update persisted
        updated_task = await service.get_task(created_task.id, "user-a")
        assert updated_task.title == "Updated Title"

    async def test_delete_task_fails_for_different_owner(
        self, test_session: AsyncSession
    ):
        """delete_task() should return False if task belongs to different user"""
        service = TaskService(test_session)

        # Create a task for user-a
        task_create = TaskCreate(title="Task to Delete")
        created_task = await service.create_task(task_create, "user-a")

        # Try to delete as user-b
        result = await service.delete_task(created_task.id, "user-b")
        assert result is False

        # Verify task still exists for user-a
        task = await service.get_task(created_task.id, "user-a")
        assert task is not None

    async def test_delete_task_succeeds_for_owner(
        self, test_session: AsyncSession
    ):
        """delete_task() should succeed if task belongs to the user"""
        service = TaskService(test_session)

        # Create a task for user-a
        task_create = TaskCreate(title="Task to Delete")
        created_task = await service.create_task(task_create, "user-a")

        # Delete as user-a
        result = await service.delete_task(created_task.id, "user-a")
        assert result is True

        # Verify task is deleted
        task = await service.get_task(created_task.id, "user-a")
        assert task is None

    async def test_mark_complete_fails_for_different_owner(
        self, test_session: AsyncSession
    ):
        """mark_complete() should return None if task belongs to different user"""
        service = TaskService(test_session)

        # Create a task for user-a
        task_create = TaskCreate(title="Task to Complete")
        created_task = await service.create_task(task_create, "user-a")
        assert created_task.is_completed is False

        # Try to mark complete as user-b
        result = await service.mark_complete(created_task.id, "user-b")
        assert result is None

        # Verify task is still incomplete for user-a
        task = await service.get_task(created_task.id, "user-a")
        assert task.is_completed is False

    async def test_mark_complete_succeeds_for_owner(
        self, test_session: AsyncSession
    ):
        """mark_complete() should succeed if task belongs to the user"""
        service = TaskService(test_session)

        # Create a task for user-a
        task_create = TaskCreate(title="Task to Complete")
        created_task = await service.create_task(task_create, "user-a")
        assert created_task.is_completed is False

        # Mark complete as user-a
        result = await service.mark_complete(created_task.id, "user-a")
        assert result is not None
        assert result.is_completed is True

        # Verify task is marked complete
        task = await service.get_task(created_task.id, "user-a")
        assert task.is_completed is True

    async def test_create_task_assigns_correct_user_id(
        self, test_session: AsyncSession
    ):
        """create_task() should assign user_id to the task"""
        service = TaskService(test_session)

        # Create task for user-a
        task_create = TaskCreate(title="New Task", description="Test task")
        created_task = await service.create_task(task_create, "user-a")

        assert created_task.user_id == "user-a"
        assert created_task.title == "New Task"
        assert created_task.description == "Test task"

    async def test_multiple_users_operations_isolated(
        self, test_session: AsyncSession
    ):
        """Complex scenario: multiple users with multiple operations"""
        service = TaskService(test_session)

        # User A creates 2 tasks
        task_a1 = await service.create_task(
            TaskCreate(title="A Task 1"), "user-a"
        )
        task_a2 = await service.create_task(
            TaskCreate(title="A Task 2"), "user-a"
        )

        # User B creates 2 tasks
        task_b1 = await service.create_task(
            TaskCreate(title="B Task 1"), "user-b"
        )
        task_b2 = await service.create_task(
            TaskCreate(title="B Task 2"), "user-b"
        )

        # User A updates their task
        await service.update_task(
            task_a1.id, "user-a", TaskUpdate(title="A Task 1 Updated")
        )

        # User B tries to update User A's task (should fail)
        result = await service.update_task(
            task_a1.id, "user-b", TaskUpdate(title="Hacked")
        )
        assert result is None

        # User A completes their task
        completed = await service.mark_complete(task_a2.id, "user-a")
        assert completed is not None
        assert completed.is_completed is True

        # Verify User B's task is still incomplete
        task_b2_check = await service.get_task(task_b2.id, "user-b")
        assert task_b2_check.is_completed is False

        # User B deletes their task
        deleted = await service.delete_task(task_b1.id, "user-b")
        assert deleted is True

        # Verify User A's task still exists
        task_a1_check = await service.get_task(task_a1.id, "user-a")
        assert task_a1_check is not None

        # Final check: each user still sees only their own tasks
        user_a_tasks = await service.get_tasks("user-a")
        user_b_tasks = await service.get_tasks("user-b")

        assert len(user_a_tasks) == 2
        assert len(user_b_tasks) == 1  # One was deleted

        assert all(t.user_id == "user-a" for t in user_a_tasks)
        assert all(t.user_id == "user-b" for t in user_b_tasks)
