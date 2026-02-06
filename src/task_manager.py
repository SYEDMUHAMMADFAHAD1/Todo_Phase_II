"""
Task Manager Module
Handles all core task operations for the todo application
"""

import uuid
from typing import List, Dict, Optional


class Task:
    """Represents a single task in the todo application"""

    def __init__(self, title: str, description: str = "", completed: bool = False):
        self.id: str = str(uuid.uuid4())
        self.title: str = title
        self.description: str = description
        self.completed: bool = completed

    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.title} - {self.description}"


class TaskManager:
    """Manages all tasks in the application"""

    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, title: str, description: str = "") -> Dict:
        """Add a new task to the task list"""
        try:
            if not isinstance(title, str) or not title.strip():
                return {"success": False, "message": "Title cannot be empty"}

            task = Task(title=title, description=description)
            self.tasks.append(task)
            return {"success": True, "task": task, "message": f"Task '{title}' added successfully"}
        except Exception as e:
            return {"success": False, "message": f"Error adding task: {str(e)}"}

    def view_tasks(self) -> List[Task]:
        """Return all tasks"""
        try:
            return self.tasks.copy()  # Return a copy to prevent external modification
        except Exception as e:
            print(f"Error retrieving tasks: {str(e)}")
            return []

    def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None) -> Dict:
        """Update an existing task"""
        try:
            if not isinstance(task_id, str):
                return {"success": False, "message": "Task ID must be a string"}

            task = self._find_task_by_id(task_id)
            if not task:
                return {"success": False, "message": f"Task with ID {task_id} not found"}

            if title is not None:
                if not isinstance(title, str) or not title.strip():
                    return {"success": False, "message": "Title cannot be empty"}
                task.title = title

            if description is not None:
                if not isinstance(description, str):
                    return {"success": False, "message": "Description must be a string"}
                task.description = description

            return {"success": True, "task": task, "message": f"Task '{task.id}' updated successfully"}
        except Exception as e:
            return {"success": False, "message": f"Error updating task: {str(e)}"}

    def delete_task(self, task_id: str) -> Dict:
        """Delete a task by ID"""
        try:
            if not isinstance(task_id, str):
                return {"success": False, "message": "Task ID must be a string"}

            task = self._find_task_by_id(task_id)
            if not task:
                return {"success": False, "message": f"Task with ID {task_id} not found"}

            self.tasks.remove(task)
            return {"success": True, "message": f"Task '{task.id}' deleted successfully"}
        except Exception as e:
            return {"success": False, "message": f"Error deleting task: {str(e)}"}

    def toggle_task_status(self, task_id: str) -> Dict:
        """Toggle the completion status of a task"""
        try:
            if not isinstance(task_id, str):
                return {"success": False, "message": "Task ID must be a string"}

            task = self._find_task_by_id(task_id)
            if not task:
                return {"success": False, "message": f"Task with ID {task_id} not found"}

            task.completed = not task.completed
            status = "completed" if task.completed else "incomplete"
            return {"success": True, "task": task, "message": f"Task '{task.id}' marked as {status}"}
        except Exception as e:
            return {"success": False, "message": f"Error toggling task status: {str(e)}"}

    def _find_task_by_id(self, task_id: str) -> Optional[Task]:
        """Helper method to find a task by its ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


# Global task manager instance
task_manager = TaskManager()