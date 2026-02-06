import requests
import json
import uuid

# Test to verify the delete functionality works properly
BASE_URL = "http://localhost:8000"

def test_delete_functionality():
    print("Testing delete functionality...")
    
    # Create a test user
    signup_data = {
        "email": f"testuser_{uuid.uuid4().hex[:8]}@example.com",
        "password": "securepassword123",
        "name": "Test User"
    }
    
    try:
        # Sign up a new user
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        if response.status_code == 200:
            print("[PASS] Signup successful")
            result = response.json()
            token = result.get('token')
            
            if token:
                print("[PASS] Token received")
                
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
                if response.status_code == 201:
                    print("[PASS] Task creation successful")
                    task = response.json()
                    task_id = task.get('id')
                    
                    if task_id:
                        # Verify the task exists by fetching all tasks
                        response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
                        if response.status_code == 200:
                            tasks_before = response.json()
                            print(f"[INFO] Tasks before deletion: {len(tasks_before)}")
                            
                            # Test deleting the task
                            response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
                            if response.status_code == 204:
                                print("[PASS] Task deletion successful (204 No Content)")
                                
                                # Verify the task is gone by fetching all tasks again
                                response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
                                if response.status_code == 200:
                                    tasks_after = response.json()
                                    print(f"[INFO] Tasks after deletion: {len(tasks_after)}")
                                    
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
                                else:
                                    print(f"[FAIL] Fetch tasks after deletion failed: {response.status_code}")
                            else:
                                print(f"[FAIL] Task deletion failed: {response.status_code}")
                        else:
                            print(f"[FAIL] Fetch tasks before deletion failed: {response.status_code}")
                    else:
                        print("[FAIL] No task ID returned from creation")
                else:
                    print(f"[FAIL] Task creation failed: {response.status_code}, Response: {response.text}")
            else:
                print("[FAIL] No token received from signup")
        else:
            print(f"[FAIL] Signup failed: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"[FAIL] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    success = test_delete_functionality()
    if success:
        print("\n[PASS] Delete functionality test PASSED!")
    else:
        print("\n[FAIL] Delete functionality test FAILED!")