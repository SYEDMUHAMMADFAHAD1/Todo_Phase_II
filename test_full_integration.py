import asyncio
import os
import sys
sys.path.insert(0, '.')

os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./test.db'
os.environ['BETTER_AUTH_SECRET'] = 'test_secret_for_development_that_is_at_least_32_characters_long'

from fastapi.testclient import TestClient
from backend.src.main import app
import json

client = TestClient(app)

print("=" * 60)
print("FULL INTEGRATION TEST")
print("=" * 60)

# 1. Check health
print("\n1. Health Check:")
resp = client.get("/health")
print(f"   Status: {resp.status_code}")
print(f"   Response: {resp.json()}")

# 2. Test signup
print("\n2. Signup:")
signup_data = {
    "email": "testuser@example.com",
    "password": "password123",
    "name": "Test User"
}
resp = client.post("/api/auth/signup", json=signup_data)
print(f"   Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    token = data.get('token')
    user_id = data.get('user', {}).get('id')
    print(f"   Token received: {token[:20]}...")
    print(f"   User ID: {user_id}")
else:
    print(f"   Error: {resp.json()}")

# 3. Test create task without token
print("\n3. Create Task WITHOUT Token:")
task_data = {
    "title": "Test Task",
    "description": "A test task"
}
resp = client.post("/api/tasks", json=task_data)
print(f"   Status: {resp.status_code}")
print(f"   Response: {resp.json()}")

# 4. Test create task WITH token
if 'token' in locals():
    print(f"\n4. Create Task WITH Token:")
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post("/api/tasks", json=task_data, headers=headers)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 201:
        task = resp.json()
        print(f"   Task created: {task}")
    else:
        print(f"   Error: {resp.json()}")
    
    # 5. Test fetch tasks
    print(f"\n5. Fetch Tasks:")
    resp = client.get("/api/tasks", headers=headers)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        tasks = resp.json()
        print(f"   Tasks count: {len(tasks)}")
        if tasks:
            print(f"   First task: {tasks[0]}")
    else:
        print(f"   Error: {resp.json()}")
