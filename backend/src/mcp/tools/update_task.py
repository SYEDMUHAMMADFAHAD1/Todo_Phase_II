"""
Update Task MCP Tool

This module implements the update_task MCP tool for updating existing tasks.
"""
from mcp.server import Server
from mcp.types import Tool
from typing import Dict, Any
from sqlalchemy import select
from datetime import datetime

from ...models.task import Task
from ...core.db import get_session


async def update_task_impl(task_id: str, title: str = None, description: str = None, user_id: str = None) -> dict:
    """
    Implementation of the update_task functionality.

    Args:
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)
        user_id: The ID of the user who owns the task

    Returns:
        Dict with success status and updated task
    """
    try:
        # Validate inputs
        if not task_id or len(task_id.strip()) == 0:
            return {"success": False, "error": "Task ID is required"}

        if title is not None and len(title) > 255:
            return {"success": False, "error": "Title exceeds maximum length of 255 characters"}

        # Get database session
        async for db in get_session():
            try:
                # Find the task that belongs to the user
                query = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                result = await db.execute(query)
                task = result.scalar_one_or_none()

                if not task:
                    return {"success": False, "error": "Task not found or not owned by user"}

                # Update the task fields if provided
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description

                # Update the timestamp
                task.updated_at = datetime.utcnow()

                # Commit the changes
                await db.commit()
                await db.refresh(task)

                # Convert to dict format
                task_dict = {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }

                return {"success": True, "task": task_dict, "message": f"Task '{task.title}' updated successfully"}
            except Exception as db_error:
                await db.rollback()
                return {"success": False, "error": f"Database error: {str(db_error)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Define the MCP tool
update_task_tool = Tool(
    name="update_task",
    description="Updates task title and/or description. Validates task ownership.",
    inputSchema={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "string",
                "description": "The ID of the task to update"
            },
            "title": {
                "type": "string",
                "description": "New title for the task"
            },
            "description": {
                "type": "string",
                "description": "New description for the task"
            }
        },
        "required": ["task_id"]
    }
)
