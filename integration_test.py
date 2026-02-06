import requests
import json
import uuid

# Integration test to verify the fix
BASE_URL = "http://localhost:8000"

def test_authentication_and_tasks():
    print("Testing authentication and task operations...")
    
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
                    "title": "Test task from integration test",
                    "description": "This is a test task"
                }
                
                response = requests.post(f"{BASE_URL}/api/tasks", json=task_data, headers=headers)
                if response.status_code == 201:
                    print("[PASS] Task creation successful")
                    task = response.json()
                    task_id = task.get('id')
                    
                    if task_id:
                        # Test fetching tasks
                        response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
                        if response.status_code == 200:
                            tasks = response.json()
                            print(f"[PASS] Fetched {len(tasks)} tasks")
                            
                            # Test updating the task
                            update_data = {
                                "title": "Updated test task",
                                "is_completed": True
                            }
                            response = requests.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_data, headers=headers)
                            if response.status_code == 200:
                                print("[PASS] Task update successful")
                                
                                # Test deleting the task
                                response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
                                if response.status_code == 204:
                                    print("[PASS] Task deletion successful")
                                    print("\n[SUCCESS] All tests passed! The API is working correctly.")
                                    return True
                                else:
                                    print(f"[FAIL] Task deletion failed: {response.status_code}")
                            else:
                                print(f"[FAIL] Task update failed: {response.status_code}")
                        else:
                            print(f"[FAIL] Fetch tasks failed: {response.status_code}")
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
    
    return False

if __name__ == "__main__":
    success = test_authentication_and_tasks()
    if success:
        print("\n[PASS] Integration test PASSED - All API operations working correctly!")
    else:
        print("\n[FAIL] Integration test FAILED - There are still issues with the API")