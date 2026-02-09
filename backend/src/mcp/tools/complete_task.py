"""
Complete Task MCP Tool

This module implements the complete_task MCP tool for marking tasks as completed.
"""
from mcp.server import Server
from mcp.types import Tool
from typing import Dict, Any
from sqlalchemy import select
from datetime import datetime

from ...models.task import Task
from ...core.db import get_session


async def complete_task_impl(task_id: str, user_id: str = None) -> dict:
    """
    Implementation of the complete_task functionality.

    Args:
        task_id: The ID of the task to mark as completed
        user_id: The ID of the user who owns the task

    Returns:
        Dict with success status and completed task
    """
    try:
        # Validate inputs
        if not task_id or len(task_id.strip()) == 0:
            return {"success": False, "error": "Task ID is required"}

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

                # Mark the task as completed (idempotent operation)
                task.is_completed = True
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

                return {"success": True, "task": task_dict, "message": f"Task '{task.title}' marked as completed"}
            except Exception as db_error:
                await db.rollback()
                return {"success": False, "error": f"Database error: {str(db_error)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Define the MCP tool
complete_task_tool = Tool(
    name="complete_task",
    description="Marks a task as completed. Idempotent behavior preferred.",
    inputSchema={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "string",
                "description": "The ID of the task to mark as completed"
            }
        },
        "required": ["task_id"]
    }
)
