#!/usr/bin/env python3
"""
Test script to validate all features of the todo application
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from task_manager import task_manager


def test_add_task():
    """Test adding a task"""
    print("Testing add_task functionality...")

    # Test adding a valid task
    result = task_manager.add_task("Test Task", "This is a test task")
    assert result["success"] == True, f"Expected success, got {result}"
    assert len(task_manager.view_tasks()) == 1, f"Expected 1 task, got {len(task_manager.view_tasks())}"
    print("PASS: Add task test passed")


def test_view_tasks():
    """Test viewing tasks"""
    print("Testing view_tasks functionality...")

    tasks = task_manager.view_tasks()
    assert isinstance(tasks, list), f"Expected list, got {type(tasks)}"
    print("PASS: View tasks test passed")


def test_update_task():
    """Test updating a task"""
    print("Testing update_task functionality...")

    # Add a task first
    add_result = task_manager.add_task("Original Task", "Original description")
    assert add_result["success"] == True

    # Get the task ID
    tasks = task_manager.view_tasks()
    task_to_update = tasks[-1]  # Get the last added task

    # Update the task
    update_result = task_manager.update_task(task_to_update.id, "Updated Task", "Updated description")
    assert update_result["success"] == True, f"Expected success, got {update_result}"

    # Verify the update
    updated_tasks = task_manager.view_tasks()
    updated_task = None
    for t in updated_tasks:
        if t.id == task_to_update.id:
            updated_task = t
            break

    assert updated_task is not None, "Task not found after update"
    assert updated_task.title == "Updated Task", f"Expected 'Updated Task', got '{updated_task.title}'"
    assert updated_task.description == "Updated description", f"Expected 'Updated description', got '{updated_task.description}'"
    print("PASS: Update task test passed")


def test_toggle_task_status():
    """Test toggling task status"""
    print("Testing toggle_task_status functionality...")

    # Add a task
    add_result = task_manager.add_task("Toggle Test Task", "Task for toggling")
    assert add_result["success"] == True

    # Get the task ID
    tasks = task_manager.view_tasks()
    task_to_toggle = tasks[-1]  # Get the last added task

    # Verify initial status
    assert task_to_toggle.completed == False, f"Expected completed=False, got {task_to_toggle.completed}"

    # Toggle the status
    toggle_result = task_manager.toggle_task_status(task_to_toggle.id)
    assert toggle_result["success"] == True, f"Expected success, got {toggle_result}"

    # Verify the toggle
    toggled_tasks = task_manager.view_tasks()
    toggled_task = None
    for t in toggled_tasks:
        if t.id == task_to_toggle.id:
            toggled_task = t
            break

    assert toggled_task is not None, "Task not found after toggle"
    assert toggled_task.completed == True, f"Expected completed=True, got {toggled_task.completed}"

    # Toggle again to return to original state
    toggle_result2 = task_manager.toggle_task_status(toggled_task.id)
    assert toggle_result2["success"] == True, f"Expected success, got {toggle_result2}"

    # Verify the second toggle
    final_tasks = task_manager.view_tasks()
    final_task = None
    for t in final_tasks:
        if t.id == toggled_task.id:
            final_task = t
            break

    assert final_task is not None, "Task not found after second toggle"
    assert final_task.completed == False, f"Expected completed=False, got {final_task.completed}"
    print("PASS: Toggle task status test passed")


def test_delete_task():
    """Test deleting a task"""
    print("Testing delete_task functionality...")

    # Add a task
    add_result = task_manager.add_task("Delete Test Task", "Task for deletion")
    assert add_result["success"] == True

    initial_count = len(task_manager.view_tasks())

    # Get the task ID
    tasks = task_manager.view_tasks()
    task_to_delete = tasks[-1]  # Get the last added task

    # Delete the task
    delete_result = task_manager.delete_task(task_to_delete.id)
    assert delete_result["success"] == True, f"Expected success, got {delete_result}"

    # Verify the deletion
    final_count = len(task_manager.view_tasks())
    assert final_count == initial_count - 1, f"Expected {initial_count - 1} tasks, got {final_count}"
    print("PASS: Delete task test passed")


def test_error_handling():
    """Test error handling for invalid inputs"""
    print("Testing error handling...")

    # Test adding task with empty title
    result = task_manager.add_task("", "Description with empty title")
    assert result["success"] == False, f"Expected failure for empty title, got {result}"

    # Test updating non-existent task
    result = task_manager.update_task("non-existent-id", "New Title")
    assert result["success"] == False, f"Expected failure for non-existent task, got {result}"

    # Test deleting non-existent task
    result = task_manager.delete_task("non-existent-id")
    assert result["success"] == False, f"Expected failure for non-existent task, got {result}"

    # Test toggling non-existent task
    result = task_manager.toggle_task_status("non-existent-id")
    assert result["success"] == False, f"Expected failure for non-existent task, got {result}"

    print("PASS: Error handling test passed")


def run_all_tests():
    """Run all validation tests"""
    print("Starting validation of all todo application features...\n")

    try:
        test_add_task()
        print()

        test_view_tasks()
        print()

        test_update_task()
        print()

        test_toggle_task_status()
        print()

        test_delete_task()
        print()

        test_error_handling()
        print()

        print("SUCCESS: All tests passed! The todo application is working correctly.")
        print("FEATURE: Adding tasks")
        print("FEATURE: Viewing task list")
        print("FEATURE: Updating tasks")
        print("FEATURE: Deleting tasks")
        print("FEATURE: Marking tasks complete/incomplete")
        print("FEATURE: Handling invalid input gracefully")

    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during testing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()