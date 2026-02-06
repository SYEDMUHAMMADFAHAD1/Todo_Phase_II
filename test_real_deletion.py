import requests
import json
import uuid
import sqlite3
import time

# Test to check if deletion actually affects the database
BASE_URL = "http://localhost:8000"
DB_PATH = r"C:\master_second_copy\Todo_App\backend\todo_app.db"

def count_tasks_in_db():
    """Count tasks in the database directly"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM task;')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Error counting tasks in DB: {e}")
        return -1

def test_real_deletion():
    print("Testing real deletion by checking database directly...")
    print(f"Initial task count in DB: {count_tasks_in_db()}")
    
    # Create a test user
    signup_data = {
        "email": f"testuser_{uuid.uuid4().hex[:8]}@example.com",
        "password": "securepassword123",
        "name": "Test User"
    }
    
    try:
        # Sign up a new user
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        if response.status_code != 200:
            print(f"Signup failed: {response.text}")
            return False
            
        result = response.json()
        token = result.get('token')
        if not token:
            print("No token received")
            return False

        # Set up headers with the token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Create a task
        task_data = {
            "title": "Test task for deletion verification",
            "description": "This task will be deleted"
        }

        response = requests.post(f"{BASE_URL}/api/tasks", json=task_data, headers=headers)
        if response.status_code != 201:
            print(f"Task creation failed: {response.text}")
            return False
            
        task = response.json()
        task_id = task.get('id')
        print(f"Created task ID: {task_id}")
        
        if not task_id:
            print("No task ID returned")
            return False

        # Check DB count after creation
        after_creation = count_tasks_in_db()
        print(f"Task count in DB after creation: {after_creation}")

        # Delete the task
        response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
        print(f"Delete response: {response.status_code}")
        if response.status_code != 204:
            print(f"Delete failed: {response.text}")
            return False

        # Check DB count after deletion
        after_deletion = count_tasks_in_db()
        print(f"Task count in DB after deletion: {after_deletion}")

        if after_deletion < after_creation:
            print("[SUCCESS] Database task count decreased after deletion!")
            return True
        else:
            print(f"[FAILURE] Database task count did not decrease: {after_creation} -> {after_deletion}")
            return False

    except Exception as e:
        print(f"Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_real_deletion()
    if success:
        print("\n[SUCCESS] Real deletion test PASSED!")
    else:
        print("\n[FAILURE] Real deletion test FAILED!")