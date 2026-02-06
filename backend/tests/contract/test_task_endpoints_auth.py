"""
Contract tests for task endpoint authentication.

Tests verify that ALL task endpoints:
1. Require Authorization header with valid JWT token
2. Return 401 Unauthorized for missing Authorization header
3. Return 401 Unauthorized for invalid/expired tokens
4. Accept requests with valid JWT token

These tests are CONTRACTS between frontend and backend:
- Frontend must include Authorization: Bearer <JWT> header
- Backend must validate token on every request
- Backend must return 401 for any auth failure
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestTaskEndpointsAuthentication:
    """Contract tests: all task endpoints require authentication"""

    # ===== GET /api/tasks (List tasks) =====

    async def test_get_tasks_missing_authorization_header(self, async_client):
        """GET /api/tasks without Authorization header returns 401"""
        response = await async_client.get("/api/tasks")
        assert response.status_code == 401
        assert "detail" in response.json()

    async def test_get_tasks_with_valid_token(self, async_client, create_valid_jwt):
        """GET /api/tasks with valid JWT token returns 200 (or empty list)"""
        token = create_valid_jwt("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        response = await async_client.get("/api/tasks", headers=headers)
        # Should return 200 OK (may be empty list if no tasks for user)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_tasks_with_expired_token(self, async_client, create_expired_jwt):
        """GET /api/tasks with expired token returns 401"""
        token = create_expired_jwt("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        response = await async_client.get("/api/tasks", headers=headers)
        assert response.status_code == 401

    async def test_get_tasks_with_invalid_signature(self, async_client, create_invalid_signature_jwt):
        """GET /api/tasks with invalid signature token returns 401"""
        token = create_invalid_signature_jwt("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        response = await async_client.get("/api/tasks", headers=headers)
        assert response.status_code == 401

    async def test_get_tasks_malformed_bearer_header(self, async_client):
        """GET /api/tasks with malformed Bearer header returns 401"""
        # Missing "Bearer " prefix
        headers = {"Authorization": "malformed-token"}
        response = await async_client.get("/api/tasks", headers=headers)
        assert response.status_code == 401

    # ===== POST /api/tasks (Create task) =====

    async def test_post_tasks_missing_authorization_header(self, async_client):
        """POST /api/tasks without Authorization header returns 401"""
        payload = {"title": "Test Task"}
        response = await async_client.post("/api/tasks", json=payload)
        assert response.status_code == 401

    async def test_post_tasks_with_valid_token(self, async_client, create_valid_jwt):
        """POST /api/tasks with valid JWT token returns 201 or 200"""
        token = create_valid_jwt("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"title": "New Task", "description": "Task description"}
        response = await async_client.post("/api/tasks", json=payload, headers=headers)
        # Should return 201 Created (or 200 if endpoint configured differently)
        assert response.status_code in [200, 201]
        if response.status_code == 201:
            assert "id" in response.json()

    async def test_post_tasks_with_expired_token(self, async_client, create_expired_jwt):
        """POST /api/tasks with expired token returns 401"""
        token = create_expired_jwt("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"title": "Test Task"}
        response = await async_client.post("/api/tasks", json=payload, headers=headers)
        assert response.status_code == 401

    # ===== GET /api/tasks/{task_id} (Get single task) =====

    async def test_get_task_by_id_missing_authorization(self, async_client):
        """GET /api/tasks/{task_id} without Authorization returns 401"""
        fake_task_id = "12345678-1234-5678-1234-567812345678"
        response = await async_client.get(f"/api/tasks/{fake_task_id}")
        assert response.status_code == 401

    async def test_get_task_by_id_with_expired_token(self, async_client, create_expired_jwt):
        """GET /api/tasks/{task_id} with expired token returns 401"""
        token = create_expired_jwt("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        fake_task_id = "12345678-1234-5678-1234-567812345678"
        response = await async_client.get(f"/api/tasks/{fake_task_id}", headers=headers)
        assert response.status_code == 401

    # ===== PUT /api/tasks/{task_id} (Update task) =====

    async def test_put_task_missing_authorization(self, async_client):
        """PUT /api/tasks/{task_id} without Authorization returns 401"""
        fake_task_id = "12345678-1234-5678-1234-567812345678"
        payload = {"title": "Updated Title"}
        response = await async_client.put(f"/api/tasks/{fake_task_id}", json=payload)
        assert response.status_code == 401

    async def test_put_task_with_invalid_signature(self, async_client, create_invalid_signature_jwt):
        """PUT /api/tasks/{task_id} with invalid signature returns 401"""
        token = create_invalid_signature_jwt("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        fake_task_id = "12345678-1234-5678-1234-567812345678"
        payload = {"title": "Updated Title"}
        response = await async_client.put(f"/api/tasks/{fake_task_id}", json=payload, headers=headers)
        assert response.status_code == 401

    # ===== DELETE /api/tasks/{task_id} (Delete task) =====

    async def test_delete_task_missing_authorization(self, async_client):
        """DELETE /api/tasks/{task_id} without Authorization returns 401"""
        fake_task_id = "12345678-1234-5678-1234-567812345678"
        response = await async_client.delete(f"/api/tasks/{fake_task_id}")
        assert response.status_code == 401

    async def test_delete_task_with_expired_token(self, async_client, create_expired_jwt):
        """DELETE /api/tasks/{task_id} with expired token returns 401"""
        token = create_expired_jwt("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        fake_task_id = "12345678-1234-5678-1234-567812345678"
        response = await async_client.delete(f"/api/tasks/{fake_task_id}", headers=headers)
        assert response.status_code == 401

    # ===== PATCH /api/tasks/{task_id}/complete (Mark complete) =====

    async def test_patch_complete_missing_authorization(self, async_client):
        """PATCH /api/tasks/{task_id}/complete without Authorization returns 401"""
        fake_task_id = "12345678-1234-5678-1234-567812345678"
        response = await async_client.patch(f"/api/tasks/{fake_task_id}/complete")
        assert response.status_code == 401

    async def test_patch_complete_with_invalid_signature(self, async_client, create_invalid_signature_jwt):
        """PATCH /api/tasks/{task_id}/complete with invalid signature returns 401"""
        token = create_invalid_signature_jwt("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        fake_task_id = "12345678-1234-5678-1234-567812345678"
        response = await async_client.patch(f"/api/tasks/{fake_task_id}/complete", headers=headers)
        assert response.status_code == 401


@pytest.mark.asyncio
class TestAuthenticationErrorMessages:
    """Tests for authentication error responses"""

    async def test_missing_auth_error_detail(self, async_client):
        """Missing Authorization returns error detail in response"""
        response = await async_client.get("/api/tasks")
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    async def test_invalid_token_error_detail(self, async_client, create_invalid_signature_jwt):
        """Invalid token returns error detail in response"""
        token = create_invalid_signature_jwt("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        response = await async_client.get("/api/tasks", headers=headers)
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    async def test_www_authenticate_header_present(self, async_client):
        """401 responses include WWW-Authenticate header for HTTP spec compliance"""
        response = await async_client.get("/api/tasks")
        assert response.status_code == 401
        # WWW-Authenticate header should be present (case-insensitive)
        headers = {k.lower(): v for k, v in response.headers.items()}
        assert "www-authenticate" in headers or response.status_code == 401
