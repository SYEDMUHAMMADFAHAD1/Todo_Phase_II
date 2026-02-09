"""
MCP Server Initialization Module

This module sets up the MCP server and provides access to task-related tools.
"""
import asyncio
from typing import Dict, Any, List

# Import the actual tool implementations from the tools directory
from .tools.add_task import add_task_tool, add_task_impl
from .tools.list_tasks import list_tasks_tool, list_tasks_impl
from .tools.update_task import update_task_tool, update_task_impl
from .tools.complete_task import complete_task_tool, complete_task_impl
from .tools.delete_task import delete_task_tool, delete_task_impl


class MCPServer:
    """Lightweight wrapper for MCP tools used by the chatbot."""

    def __init__(self):
        self.tools = {
            "add_task": add_task_impl,
            "list_tasks": list_tasks_impl,
            "update_task": update_task_impl,
            "complete_task": complete_task_impl,
            "delete_task": delete_task_impl
        }
        self.tool_definitions = [
            add_task_tool,
            list_tasks_tool,
            update_task_tool,
            complete_task_tool,
            delete_task_tool
        ]

    def get_tools(self):
        """Return the registered tool definitions."""
        return self.tool_definitions

    def get_tool_implementations(self):
        """Return the tool implementation functions."""
        return self.tools


# Global server instance
mcp_server_instance = None


def get_mcp_server() -> MCPServer:
    """Get the global MCP server instance."""
    global mcp_server_instance
    if mcp_server_instance is None:
        mcp_server_instance = MCPServer()
    return mcp_server_instance
