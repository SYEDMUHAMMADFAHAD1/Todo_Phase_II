#!/usr/bin/env python3
"""
Todo Application - Main Entry Point
This is the console-based todo application entry point.
"""

from task_manager import task_manager


def main():
    """Main application function"""
    print("Welcome to the Todo Application!")
    print("This is the console-based todo application.")

    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Task Status")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            add_task_menu()
        elif choice == '2':
            view_tasks_menu()
        elif choice == '3':
            update_task_menu()
        elif choice == '4':
            delete_task_menu()
        elif choice == '5':
            toggle_task_status_menu()
        elif choice == '6':
            print("👋 Program exited successfully")
            break
        else:
            print("⚠️ Invalid option, please try again")


def add_task_menu():
    """Menu for adding a new task"""
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty!")
        return

    description = input("Enter task description (optional): ").strip()

    result = task_manager.add_task(title, description)
    if result["success"]:
        print("✅ Task saved successfully")
    else:
        print(f"❌ Error: {result['message']}")


def view_tasks_menu():
    """Menu for viewing all tasks"""
    tasks = task_manager.view_tasks()

    if not tasks:
        print("ℹ️ No tasks available")
        return

    print("\nYour Tasks:")
    for i, task in enumerate(tasks, 1):
        status = "✓" if task.completed else "○"
        print(f"{i}. [{status}] {task.title} - {task.description} (ID: {task.id})")
    print("📋 Tasks loaded successfully")


def update_task_menu():
    """Menu for updating an existing task"""
    view_tasks_menu()

    if not task_manager.view_tasks():
        return

    task_id = input("\nEnter the task ID to update: ").strip()

    print("Leave blank to keep current value.")
    new_title = input(f"Enter new title: ").strip()
    new_description = input(f"Enter new description: ").strip()

    # Prepare update parameters
    title = new_title if new_title else None
    description = new_description if new_description else None

    # If both are empty strings, set them to None to keep original values
    if title == "":
        title = None
    if description == "":
        description = None

    result = task_manager.update_task(task_id, title, description)
    if result["success"]:
        print("✏️ Task updated successfully")
    else:
        print(f"❌ Error: {result['message']}")


def delete_task_menu():
    """Menu for deleting a task"""
    view_tasks_menu()

    if not task_manager.view_tasks():
        return

    task_id = input("\nEnter the task ID to delete: ").strip()
    result = task_manager.delete_task(task_id)
    if result["success"]:
        print("🗑️ Task deleted successfully")
    else:
        print(f"❌ Error: {result['message']}")


def toggle_task_status_menu():
    """Menu for toggling a task's completion status"""
    view_tasks_menu()

    if not task_manager.view_tasks():
        return

    task_id = input("\nEnter the task ID to toggle: ").strip()
    result = task_manager.toggle_task_status(task_id)
    if result["success"]:
        print("🔁 Task status updated successfully")
    else:
        print(f"❌ Error: {result['message']}")


if __name__ == "__main__":
    main()