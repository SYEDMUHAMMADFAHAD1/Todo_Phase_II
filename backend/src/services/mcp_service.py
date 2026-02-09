"""
MCP Service Layer

This module provides a service layer for MCP tools integration with the existing application.
"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.src.database import get_db
from backend.src.mcp.server import get_mcp_server
from backend.src.mcp.auth import validate_jwt_token
from backend.src.services.task_service import TaskService


class MCPService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.task_service = TaskService(db_session)
        self.mcp_server = get_mcp_server()
    
    async def execute_mcp_tool(self, tool_name: str, params: Dict[str, Any], authorization_header: str) -> Dict[str, Any]:
        """
        Execute an MCP tool with proper authentication and authorization.
        
        Args:
            tool_name: The name of the tool to execute
            params: Parameters for the tool
            authorization_header: The authorization header containing the JWT token
            
        Returns:
            Result from the tool execution
        """
        # Validate the JWT token and extract user ID
        user_id = self._validate_and_extract_user_id(authorization_header)
        
        # Create context for the tool execution
        context = {
            "user_id": user_id,
            "db_session": self.db_session
        }
        
        # Get the tool from the server
        server = self.mcp_server.get_server()
        
        # Execute the appropriate tool based on the name
        if tool_name == "add_task":
            from backend.src.mcp.tools.add_task import add_task_impl
            return await add_task_impl(
                title=params.get("title"),
                description=params.get("description"),
                user_id=user_id
            )
        elif tool_name == "list_tasks":
            from backend.src.mcp.tools.list_tasks import list_tasks_impl
            return await list_tasks_impl(
                filter_param=params.get("filter", "all"),
                user_id=user_id
            )
        elif tool_name == "update_task":
            from backend.src.mcp.tools.update_task import update_task_impl
            return await update_task_impl(
                task_id=params.get("task_id"),
                title=params.get("title"),
                description=params.get("description"),
                user_id=user_id
            )
        elif tool_name == "complete_task":
            from backend.src.mcp.tools.complete_task import complete_task_impl
            return await complete_task_impl(
                task_id=params.get("task_id"),
                user_id=user_id
            )
        elif tool_name == "delete_task":
            from backend.src.mcp.tools.delete_task import delete_task_impl
            return await delete_task_impl(
                task_id=params.get("task_id"),
                user_id=user_id
            )
        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}
    
    def _validate_and_extract_user_id(self, authorization_header: str) -> str:
        """
        Validate the JWT token and extract the user ID.
        
        Args:
            authorization_header: The authorization header containing the JWT token
            
        Returns:
            The user ID from the token
        """
        from backend.src.mcp.auth import get_user_id_from_token
        return get_user_id_from_token(authorization_header)
    
    def get_available_tools(self) -> list:
        """
        Get a list of available MCP tools.
        
        Returns:
            List of available tool names
        """
        return [
            "add_task",
            "list_tasks", 
            "update_task",
            "complete_task",
            "delete_task"
        ]