"""
Base Tool Handler

This module provides common functionality for all MCP tools.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
from sqlalchemy.orm import Session
from backend.src.database import get_db
from backend.src.models.task import Task
from backend.src.services.task_service import TaskService


class BaseToolHandler(ABC):
    """Abstract base class for all MCP tool handlers"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.task_service = TaskService(db_session)
    
    @abstractmethod
    async def execute(self, params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Execute the tool with the given parameters"""
        pass
    
    def validate_user_ownership(self, task_id: str, user_id: str) -> bool:
        """Validate that the user owns the specified task"""
        task = self.db_session.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()
        
        return task is not None