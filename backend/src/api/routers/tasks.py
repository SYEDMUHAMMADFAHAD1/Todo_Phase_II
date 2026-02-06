import uuid
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import UserIdentity, get_current_user
from backend.src.core.db import get_session
from backend.src.models.task import TaskRead, TaskCreate, TaskUpdate
from backend.src.services.task_service import TaskService

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter()


async def get_task_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskService:
    return TaskService(session)


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    current_user: Annotated[UserIdentity, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    """Create a new task for the authenticated user.

    Requires: Valid JWT token in Authorization header
    Returns: 201 Created with new task details
    Errors: 401 Unauthorized if missing/invalid token
    """
    try:
        logger.info(f"Creating task for user {current_user.id}: {task_in.title}")
        result = await service.create_task(task_in, current_user.id)
        logger.info(f"Task created successfully: {result.id}")

        # Convert to TaskRead format to handle UUID/string conversion
        return TaskRead.from_orm(result)
    except Exception as e:
        logger.error(f"Error creating task: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@router.get("/tasks", response_model=list[TaskRead])
async def list_tasks(
    current_user: Annotated[UserIdentity, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
    skip: int = 0,
    limit: int = 100,
):
    """List all tasks for the authenticated user.

    Requires: Valid JWT token in Authorization header
    Returns: 200 OK with list of user's tasks
    Errors: 401 Unauthorized if missing/invalid token
    """
    tasks = await service.get_tasks(current_user.id, skip=skip, limit=limit)
    # Convert each task to TaskRead format
    return [TaskRead.from_orm(task) for task in tasks]


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: str,  # Changed from uuid.UUID to str to match database storage
    current_user: Annotated[UserIdentity, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    """Get a specific task by ID.

    Requires: Valid JWT token in Authorization header
    Returns: 200 OK with task details (only if owned by user)
    Errors:
        - 401 Unauthorized if missing/invalid token
        - 404 Not Found if task doesn't exist or not owned by user
    """
    task = await service.get_task(task_id, current_user.id)
    if not task:
        logger.warning(
            "Task not found or access denied",
            extra={
                "user_id": current_user.id,
                "task_id": task_id,
                "endpoint": "GET /api/tasks/{task_id}",
                "status_code": 404,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    # Convert to TaskRead format to handle UUID/string conversion
    return TaskRead.from_orm(task)


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: str,  # Changed from uuid.UUID to str to match database storage
    task_in: TaskUpdate,
    current_user: Annotated[UserIdentity, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    """Update a task.

    Requires: Valid JWT token in Authorization header
    Returns: 200 OK with updated task
    Errors:
        - 401 Unauthorized if missing/invalid token
        - 404 Not Found if task doesn't exist or not owned by user
    """
    task = await service.update_task(task_id, current_user.id, task_in)
    if not task:
        logger.warning(
            "Task update failed - not found or access denied",
            extra={
                "user_id": current_user.id,
                "task_id": task_id,
                "endpoint": "PUT /api/tasks/{task_id}",
                "status_code": 404,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    # Convert to TaskRead format to handle UUID/string conversion
    return TaskRead.from_orm(task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,  # Changed from uuid.UUID to str to match database storage
    current_user: Annotated[UserIdentity, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    """Delete a task.

    Requires: Valid JWT token in Authorization header
    Returns: 204 No Content on success
    Errors:
        - 401 Unauthorized if missing/invalid token
        - 404 Not Found if task doesn't exist or not owned by user
    """
    # First verify the task exists and belongs to the user
    existing_task = await service.get_task(task_id, current_user.id)
    if not existing_task:
        logger.warning(
            "Task deletion failed - not found or access denied",
            extra={
                "user_id": current_user.id,
                "task_id": task_id,
                "endpoint": "DELETE /api/tasks/{task_id}",
                "status_code": 404,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    # Task exists and belongs to user, so proceed with deletion
    success = await service.delete_task(task_id, current_user.id)
    if not success:
        # This shouldn't happen if get_task succeeded, but handle just in case
        logger.error(
            "Unexpected error during task deletion",
            extra={
                "user_id": current_user.id,
                "task_id": task_id,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to delete task"
        )

    # Return 204 No Content on successful deletion
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
async def mark_task_complete(
    task_id: str,  # Changed from uuid.UUID to str to match database storage
    current_user: Annotated[UserIdentity, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    """Mark a task as complete.

    Requires: Valid JWT token in Authorization header
    Returns: 200 OK with updated task
    Errors:
        - 401 Unauthorized if missing/invalid token
        - 404 Not Found if task doesn't exist or not owned by user
    """
    task = await service.mark_complete(task_id, current_user.id)
    if not task:
        logger.warning(
            "Task completion failed - not found or access denied",
            extra={
                "user_id": current_user.id,
                "task_id": task_id,
                "endpoint": "PATCH /api/tasks/{task_id}/complete",
                "status_code": 404,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    # Convert to TaskRead format to handle UUID/string conversion
    return TaskRead.from_orm(task)
