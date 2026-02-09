"""
MCP Task Schemas

This module defines the Pydantic models for all task-related MCP tools.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class TaskSchema(BaseModel):
    """Schema representing a task entity"""
    id: str
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    is_completed: bool = False
    user_id: str
    created_at: datetime
    updated_at: datetime


class AddTaskParams(BaseModel):
    """Parameters for the add_task MCP tool"""
    title: str = Field(..., max_length=255, description="The title of the task to create")
    description: Optional[str] = Field(None, description="The description of the task to create")


class AddTaskResult(BaseModel):
    """Result returned by the add_task MCP tool"""
    success: bool
    task_id: Optional[str] = None
    error: Optional[str] = None


class ListTasksParams(BaseModel):
    """Parameters for the list_tasks MCP tool"""
    filter: Optional[str] = Field(
        "all", 
        description="Filter for task status (all, pending, completed)",
        pattern="^(all|pending|completed)$"
    )


class ListTasksResult(BaseModel):
    """Result returned by the list_tasks MCP tool"""
    success: bool
    tasks: List[TaskSchema] = []
    error: Optional[str] = None


class UpdateTaskParams(BaseModel):
    """Parameters for the update_task MCP tool"""
    task_id: str = Field(..., description="The ID of the task to update")
    title: Optional[str] = Field(None, max_length=255, description="New title for the task")
    description: Optional[str] = Field(None, description="New description for the task")


class UpdateTaskResult(BaseModel):
    """Result returned by the update_task MCP tool"""
    success: bool
    task: Optional[TaskSchema] = None
    error: Optional[str] = None


class CompleteTaskParams(BaseModel):
    """Parameters for the complete_task MCP tool"""
    task_id: str = Field(..., description="The ID of the task to mark as completed")


class CompleteTaskResult(BaseModel):
    """Result returned by the complete_task MCP tool"""
    success: bool
    task: Optional[TaskSchema] = None
    error: Optional[str] = None


class DeleteTaskParams(BaseModel):
    """Parameters for the delete_task MCP tool"""
    task_id: str = Field(..., description="The ID of the task to delete")


class DeleteTaskResult(BaseModel):
    """Result returned by the delete_task MCP tool"""
    success: bool
    error: Optional[str] = None