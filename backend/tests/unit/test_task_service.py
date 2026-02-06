import uuid
from unittest.mock import AsyncMock, MagicMock
import pytest
from backend.src.services.task_service import TaskService
from backend.src.models.task import TaskCreate, Task

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def task_service(mock_session):
    return TaskService(mock_session)

@pytest.mark.asyncio
async def test_create_task(task_service, mock_session):
    task_create = TaskCreate(title="Test Task", description="Test Description")
    user_id = "user123"

    result = await task_service.create_task(task_create, user_id)

    assert result.title == "Test Task"
    assert result.user_id == "user123"
    assert not result.is_completed

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_tasks(task_service, mock_session):
    user_id = "user123"

    # Mock the execute result for select
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Task(id=uuid.uuid4(), title="Task 1", user_id=user_id),
        Task(id=uuid.uuid4(), title="Task 2", user_id=user_id)
    ]
    mock_session.execute.return_value = mock_result

    tasks = await task_service.get_tasks(user_id)

    assert len(tasks) == 2
    mock_session.execute.assert_awaited_once()

@pytest.mark.asyncio
async def test_mark_complete(task_service, mock_session):
    task_id = uuid.uuid4()
    user_id = "user123"

    # Mock getting the task
    mock_result = MagicMock()
    existing_task = Task(id=task_id, title="Test", user_id=user_id, is_completed=False)

    # We need to ensure sqlmodel_update works or is mocked
    # Since Task is a SQLModel which is Pydantic, it has sqlmodel_update

    mock_result.scalars.return_value.first.return_value = existing_task
    mock_session.execute.return_value = mock_result

    updated_task = await task_service.mark_complete(task_id, user_id)

    assert updated_task.is_completed is True
    mock_session.add.assert_called_once_with(existing_task)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
