import requests
import json

# Test the backend API endpoints directly
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    print("Testing API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        
    # Test tasks endpoint (should return 401 without auth)
    try:
        response = requests.get(f"{BASE_URL}/api/tasks")
        print(f"Tasks GET (no auth): {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Tasks GET failed: {e}")
        
    # Test signup endpoint structure
    try:
        response = requests.get(f"{BASE_URL}/api/docs")  # OpenAPI docs
        print(f"API Docs available: {response.status_code == 200}")
    except Exception as e:
        print(f"API Docs check failed: {e}")

if __name__ == "__main__":
    test_api_endpoints()