"""
Integration tests for multi-user task isolation.

Tests verify that:
1. User A cannot read User B's tasks
2. User A cannot modify User B's tasks
3. User A cannot delete User B's tasks
4. Each user can only see/modify their own tasks
5. Task ownership is enforced at the service layer

These tests ensure users are completely isolated and cannot access
or manipulate other users' data through the API.
"""

import pytest
from httpx import AsyncClient
import uuid


@pytest.mark.asyncio
class TestMultiUserIsolation:
    """Test that different users cannot access each other's tasks"""

    async def test_user_a_cannot_see_user_b_tasks(
        self, async_client, create_valid_jwt
    ):
        """User A creates a task, User B cannot list it"""
        # User A logs in and creates a task
        user_a_token = create_valid_jwt("user-a-123")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        task_payload = {"title": "User A Task", "description": "Only User A should see this"}
        response = await async_client.post(
            "/api/tasks", json=task_payload, headers=user_a_headers
        )
        assert response.status_code == 201
        user_a_task_id = response.json()["id"]

        # User B logs in and tries to list tasks
        user_b_token = create_valid_jwt("user-b-456")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        response = await async_client.get("/api/tasks", headers=user_b_headers)
        assert response.status_code == 200
        tasks = response.json()
        # User B's list should be empty (no User A's task)
        assert len(tasks) == 0
        assert not any(t["id"] == user_a_task_id for t in tasks)

    async def test_user_b_cannot_get_user_a_task_by_id(
        self, async_client, create_valid_jwt
    ):
        """User A creates a task, User B cannot GET it by ID"""
        # User A creates a task
        user_a_token = create_valid_jwt("user-a-123")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        task_payload = {"title": "Secret Task", "description": "User A only"}
        response = await async_client.post(
            "/api/tasks", json=task_payload, headers=user_a_headers
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        # User B tries to GET the task by ID
        user_b_token = create_valid_jwt("user-b-456")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        response = await async_client.get(
            f"/api/tasks/{task_id}", headers=user_b_headers
        )
        # Should return 404 (task not found for this user)
        assert response.status_code == 404

    async def test_user_b_cannot_update_user_a_task(
        self, async_client, create_valid_jwt
    ):
        """User A creates a task, User B cannot UPDATE it"""
        # User A creates a task
        user_a_token = create_valid_jwt("user-a-123")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        task_payload = {"title": "Original Title"}
        response = await async_client.post(
            "/api/tasks", json=task_payload, headers=user_a_headers
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        # User B tries to UPDATE the task
        user_b_token = create_valid_jwt("user-b-456")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        update_payload = {"title": "Hacked Title"}
        response = await async_client.put(
            f"/api/tasks/{task_id}", json=update_payload, headers=user_b_headers
        )
        # Should return 404 (task not found for this user)
        assert response.status_code == 404

        # Verify User A's task wasn't modified
        response = await async_client.get(
            f"/api/tasks/{task_id}", headers=user_a_headers
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Original Title"

    async def test_user_b_cannot_delete_user_a_task(
        self, async_client, create_valid_jwt
    ):
        """User A creates a task, User B cannot DELETE it"""
        # User A creates a task
        user_a_token = create_valid_jwt("user-a-123")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        task_payload = {"title": "Task to Protect"}
        response = await async_client.post(
            "/api/tasks", json=task_payload, headers=user_a_headers
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        # User B tries to DELETE the task
        user_b_token = create_valid_jwt("user-b-456")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        response = await async_client.delete(
            f"/api/tasks/{task_id}", headers=user_b_headers
        )
        # Should return 404 (task not found for this user)
        assert response.status_code == 404

        # Verify User A's task still exists
        response = await async_client.get(
            f"/api/tasks/{task_id}", headers=user_a_headers
        )
        assert response.status_code == 200

    async def test_user_b_cannot_mark_user_a_task_complete(
        self, async_client, create_valid_jwt
    ):
        """User A creates a task, User B cannot mark it complete"""
        # User A creates a task
        user_a_token = create_valid_jwt("user-a-123")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        task_payload = {"title": "Task to Complete"}
        response = await async_client.post(
            "/api/tasks", json=task_payload, headers=user_a_headers
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        # User B tries to mark it complete
        user_b_token = create_valid_jwt("user-b-456")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        response = await async_client.patch(
            f"/api/tasks/{task_id}/complete", headers=user_b_headers
        )
        # Should return 404 (task not found for this user)
        assert response.status_code == 404

        # Verify task is still incomplete for User A
        response = await async_client.get(
            f"/api/tasks/{task_id}", headers=user_a_headers
        )
        assert response.status_code == 200
        assert response.json()["is_completed"] is False

    async def test_each_user_sees_only_their_own_tasks(
        self, async_client, create_valid_jwt
    ):
        """Multiple users create tasks, each only sees their own"""
        # User A creates 2 tasks
        user_a_token = create_valid_jwt("user-a-789")
        user_a_headers = {"Authorization": f"Bearer {user_a_token}"}

        for i in range(2):
            payload = {"title": f"User A Task {i+1}"}
            await async_client.post("/api/tasks", json=payload, headers=user_a_headers)

        # User B creates 3 tasks
        user_b_token = create_valid_jwt("user-b-999")
        user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

        for i in range(3):
            payload = {"title": f"User B Task {i+1}"}
            await async_client.post("/api/tasks", json=payload, headers=user_b_headers)

        # User C creates 1 task
        user_c_token = create_valid_jwt("user-c-111")
        user_c_headers = {"Authorization": f"Bearer {user_c_token}"}

        payload = {"title": "User C Task"}
        await async_client.post("/api/tasks", json=payload, headers=user_c_headers)

        # Verify User A sees exactly 2 tasks (only their own)
        response = await async_client.get("/api/tasks", headers=user_a_headers)
        assert response.status_code == 200
        user_a_tasks = response.json()
        assert len(user_a_tasks) == 2
        assert all("User A Task" in t["title"] for t in user_a_tasks)

        # Verify User B sees exactly 3 tasks (only their own)
        response = await async_client.get("/api/tasks", headers=user_b_headers)
        assert response.status_code == 200
        user_b_tasks = response.json()
        assert len(user_b_tasks) == 3
        assert all("User B Task" in t["title"] for t in user_b_tasks)

        # Verify User C sees exactly 1 task (only their own)
        response = await async_client.get("/api/tasks", headers=user_c_headers)
        assert response.status_code == 200
        user_c_tasks = response.json()
        assert len(user_c_tasks) == 1
        assert user_c_tasks[0]["title"] == "User C Task"


@pytest.mark.asyncio
class TestTaskOwnershipEnforcement:
    """Test that task ownership is correctly enforced"""

    async def test_created_task_has_correct_user_id(
        self, async_client, create_valid_jwt
    ):
        """Created task should have user_id matching authenticated user"""
        user_token = create_valid_jwt("user-task-owner-123")
        headers = {"Authorization": f"Bearer {user_token}"}

        payload = {"title": "Ownership Test Task"}
        response = await async_client.post("/api/tasks", json=payload, headers=headers)
        assert response.status_code == 201
        task = response.json()

        # Task should have user_id matching the authenticated user
        assert task["user_id"] == "user-task-owner-123"

    async def test_multiple_users_create_tasks_with_correct_ownership(
        self, async_client, create_valid_jwt
    ):
        """Multiple users create tasks with correct ownership for each"""
        user_ids = ["user-owner-a", "user-owner-b", "user-owner-c"]
        created_tasks = {}

        for user_id in user_ids:
            token = create_valid_jwt(user_id)
            headers = {"Authorization": f"Bearer {token}"}
            payload = {"title": f"Task by {user_id}"}
            response = await async_client.post(
                "/api/tasks", json=payload, headers=headers
            )
            assert response.status_code == 201
            task = response.json()
            assert task["user_id"] == user_id
            created_tasks[user_id] = task

        # Verify no user sees another user's task
        for user_id in user_ids:
            token = create_valid_jwt(user_id)
            headers = {"Authorization": f"Bearer {token}"}
            response = await async_client.get("/api/tasks", headers=headers)
            assert response.status_code == 200
            tasks = response.json()

            # Should only have 1 task (their own)
            assert len(tasks) == 1
            assert tasks[0]["user_id"] == user_id
            assert tasks[0] == created_tasks[user_id]
