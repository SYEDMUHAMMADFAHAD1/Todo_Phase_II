"""
Delete Task MCP Tool

This module implements the delete_task MCP tool for deleting tasks.
"""
from mcp.server import Server
from mcp.types import Tool
from typing import Dict, Any
from sqlalchemy import select, delete

from ...models.task import Task
from ...core.db import get_session


async def delete_task_impl(task_id: str, user_id: str = None) -> dict:
    """
    Implementation of the delete_task functionality.

    Args:
        task_id: The ID of the task to delete
        user_id: The ID of the user who owns the task

    Returns:
        Dict with success status
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

                # Store title for message
                task_title = task.title

                # Delete the task
                await db.delete(task)
                await db.commit()

                return {"success": True, "message": f"Task '{task_title}' deleted successfully"}
            except Exception as db_error:
                await db.rollback()
                return {"success": False, "error": f"Database error: {str(db_error)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Define the MCP tool
delete_task_tool = Tool(
    name="delete_task",
    description="Deletes a task. Validates ownership before deletion.",
    inputSchema={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "string",
                "description": "The ID of the task to delete"
            }
        },
        "required": ["task_id"]
    }
)
