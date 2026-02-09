"""
Add Task MCP Tool

This module implements the add_task MCP tool for creating new tasks.
"""
from mcp.server import Server
from mcp.types import Tool
from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from ...models.task import Task
from ...core.db import get_session


async def add_task_impl(title: str, description: str = None, user_id: str = None) -> dict:
    """
    Implementation of the add_task functionality.

    Args:
        title: The title of the task to create
        description: Optional description of the task
        user_id: The ID of the user creating the task

    Returns:
        Dict with success status and task ID
    """
    try:
        # Validate inputs
        if not title or len(title.strip()) == 0:
            return {"success": False, "error": "Title is required"}

        if len(title) > 255:
            return {"success": False, "error": "Title exceeds maximum length of 255 characters"}

        # Create a new task instance
        task_id = str(uuid.uuid4())
        new_task = Task(
            id=task_id,
            title=title,
            description=description,
            is_completed=False,
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Get database session and add the task
        async for db in get_session():
            try:
                db.add(new_task)
                await db.commit()
                await db.refresh(new_task)

                return {"success": True, "task_id": task_id, "message": f"Task '{title}' created successfully"}
            except Exception as db_error:
                await db.rollback()
                return {"success": False, "error": f"Database error: {str(db_error)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Define the MCP tool
add_task_tool = Tool(
    name="add_task",
    description="Creates a new task for the authenticated user. Accepts title and optional description.",
    inputSchema={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of the task to create"
            },
            "description": {
                "type": "string",
                "description": "Optional description of the task"
            }
        },
        "required": ["title"]
    }
)