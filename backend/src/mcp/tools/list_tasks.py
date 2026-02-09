"""
List Tasks MCP Tool

This module implements the list_tasks MCP tool for retrieving user tasks.
"""
from mcp.server import Server
from mcp.types import Tool
from typing import Dict, Any, List
from sqlalchemy import select

from ...models.task import Task
from ...core.db import get_session


async def list_tasks_impl(filter_param: str = "all", user_id: str = None) -> dict:
    """
    Implementation of the list_tasks functionality.

    Args:
        filter_param: Filter for task status ('all', 'pending', 'completed')
        user_id: The ID of the user whose tasks to retrieve

    Returns:
        Dict with success status and list of tasks
    """
    try:
        # Validate inputs
        if filter_param not in ["all", "pending", "completed"]:
            return {"success": False, "tasks": [], "error": "Invalid filter parameter"}

        # Get database session
        async for db in get_session():
            try:
                # Build query based on filter
                query = select(Task).where(Task.user_id == user_id)

                if filter_param == "pending":
                    query = query.where(Task.is_completed == False)
                elif filter_param == "completed":
                    query = query.where(Task.is_completed == True)

                # Execute query and get results
                result = await db.execute(query)
                tasks = result.scalars().all()

                # Convert to dict format
                task_list = [
                    {
                        "id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "is_completed": task.is_completed,
                        "created_at": task.created_at.isoformat() if task.created_at else None,
                        "updated_at": task.updated_at.isoformat() if task.updated_at else None
                    }
                    for task in tasks
                ]

                return {"success": True, "tasks": task_list, "count": len(task_list)}
            except Exception as db_error:
                return {"success": False, "tasks": [], "error": f"Database error: {str(db_error)}"}
    except Exception as e:
        return {"success": False, "tasks": [], "error": str(e)}


# Define the MCP tool
list_tasks_tool = Tool(
    name="list_tasks",
    description="Retrieves tasks for the authenticated user. Supports filters: all, pending, completed.",
    inputSchema={
        "type": "object",
        "properties": {
            "filter": {
                "type": "string",
                "description": "Filter for task status (all, pending, completed)",
                "enum": ["all", "pending", "completed"],
                "default": "all"
            }
        },
        "required": []
    }
)