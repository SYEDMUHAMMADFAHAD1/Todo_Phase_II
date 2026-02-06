import json
import requests

API = "http://localhost:8000/api"

# Generate unique credentials
import time
email = f"test_{int(time.time())}@example.com"
password = "TestPassword123!"

print(f"🚀 Todo Creation Test")
print(f"Email: {email}")
print(f"Password: {password}")
print("")

# STEP 1: Sign Up
print("📝 STEP 1: Signing up...")
signup_response = requests.post(
    f"{API}/auth/signup",
    json={"email": email, "password": password, "name": "Test User"}
)

if signup_response.status_code != 200:
    print(f"❌ Signup failed: {signup_response.text}")
    exit(1)

signup_data = signup_response.json()
token = signup_data["token"]
user_id = signup_data["user"]["id"]

print(f"✅ Signup successful!")
print(f"   User ID: {user_id}")
print(f"   Token: {token[:30]}...")
print("")

# STEP 2: Create Todo
print("📝 STEP 2: Creating a todo...")
todo_data = {
    "title": "Build a feature to manage my tasks efficiently",
    "description": "Implement todo CRUD with proper error handling and real-time updates"
}

print(f"   Title: '{todo_data['title']}'")
print(f"   Description: '{todo_data['description']}'")
print("")

create_response = requests.post(
    f"{API}/tasks",
    json=todo_data,
    headers={"Authorization": f"Bearer {token}"}
)

print(f"   Status Code: {create_response.status_code}")
print(f"   Response: {create_response.text[:500]}")
print("")

if create_response.status_code != 201:
    print(f"❌ Create todo failed: {create_response.text}")
    exit(1)

todo = create_response.json()
print(f"✅ Todo created successfully!")
print(f"   Todo ID: {todo['id']}")
print(f"   Title: {todo['title']}")
print(f"   Status: {'Completed' if todo.get('is_completed') else 'Pending'}")
print("")

# STEP 3: Fetch Todos
print("📝 STEP 3: Fetching all todos...")
fetch_response = requests.get(
    f"{API}/tasks",
    headers={"Authorization": f"Bearer {token}"}
)

if fetch_response.status_code != 200:
    print(f"❌ Fetch todos failed: {fetch_response.text}")
    exit(1)

todos = fetch_response.json()
print(f"✅ Fetched {len(todos)} todo(s)!")
print("")

for i, t in enumerate(todos, 1):
    status = "✓" if t.get("is_completed") else " "
    print(f"   {i}. [{status}] {t['title']}")
    if t.get("description"):
        print(f"      {t['description'][:60]}...")

print("")
print("✨ ═══════════════════════════════════════════════════════════")
print("✅ ALL TESTS PASSED! Todo creation is working!")
print("✨ ═══════════════════════════════════════════════════════════")
