import requests
import json
import uuid

# More detailed test to see what's happening with delete
BASE_URL = "http://localhost:8000"

def test_delete_detailed():
    print("Testing delete functionality in detail...")
    
    # Create a test user
    signup_data = {
        "email": f"testuser_{uuid.uuid4().hex[:8]}@example.com",
        "password": "securepassword123",
        "name": "Test User"
    }
    
    try:
        # Sign up a new user
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        print(f"Signup response: {response.status_code}")
        if response.status_code != 200:
            print(f"Signup failed: {response.text}")
            return False
            
        result = response.json()
        token = result.get('token')
        print(f"Token received: {token is not None}")
        
        if not token:
            return False

        # Set up headers with the token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Test creating a task
        task_data = {
            "title": "Test task for deletion",
            "description": "This task will be deleted"
        }

        response = requests.post(f"{BASE_URL}/api/tasks", json=task_data, headers=headers)
        print(f"Task creation response: {response.status_code}")
        if response.status_code != 201:
            print(f"Task creation failed: {response.text}")
            return False
            
        task = response.json()
        task_id = task.get('id')
        print(f"Created task ID: {task_id}")
        
        if not task_id:
            print("No task ID returned from creation")
            return False

        # Verify the task exists by fetching all tasks
        response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
        print(f"Fetch tasks before deletion: {response.status_code}")
        if response.status_code != 200:
            print(f"Fetch tasks failed: {response.text}")
            return False
            
        tasks_before = response.json()
        print(f"Tasks before deletion: {len(tasks_before)}")
        print(f"Task IDs before: {[t['id'] for t in tasks_before]}")

        # Try to get the specific task
        response = requests.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
        print(f"Get specific task: {response.status_code}")
        if response.status_code != 200:
            print(f"Get specific task failed: {response.text}")
            print(f"This might indicate the ID format is incorrect")
        else:
            print(f"Specific task retrieval successful")

        # Test deleting the task
        response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
        print(f"Delete response: {response.status_code}")
        if response.status_code != 204:
            print(f"Task deletion failed: {response.status_code}, Response: {response.text}")
            return False

        # Verify the task is gone by fetching all tasks again
        response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
        print(f"Fetch tasks after deletion: {response.status_code}")
        if response.status_code != 200:
            print(f"Fetch tasks after deletion failed: {response.text}")
            return False
            
        tasks_after = response.json()
        print(f"Tasks after deletion: {len(tasks_after)}")
        print(f"Task IDs after: {[t['id'] for t in tasks_after] if tasks_after else []}")

        if len(tasks_after) == len(tasks_before) - 1:
            print("[PASS] Task count decreased by 1 after deletion")
            
            # Verify the specific task is not in the list anymore
            task_exists = any(t['id'] == task_id for t in tasks_after)
            if not task_exists:
                print("[PASS] Specific task no longer appears in the list")
                print("\n[SUCCESS] All delete functionality tests passed!")
                return True
            else:
                print("[FAIL] Task still appears in the list after deletion")
        else:
            print(f"[FAIL] Task count didn't decrease properly: {len(tasks_before)} -> {len(tasks_after)}")
            
    except Exception as e:
        print(f"[FAIL] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    success = test_delete_detailed()
    if success:
        print("\n[PASS] Detailed delete functionality test PASSED!")
    else:
        print("\n[FAIL] Detailed delete functionality test FAILED!")