# Implementation Quickstart

Date: 2026-01-10 | Feature: Authentication & API Security | Branch: 002-auth-api-security

## Overview

This guide walks through implementing JWT-based authentication across all FastAPI endpoints. The backend already has JWT verification logic (backend/auth.py); this phase integrates it into task endpoints.

## Prerequisites

- FastAPI app running
- JWT verification logic complete in backend/auth.py
- Task model with user_id field
- Task service layer implemented
- .env file with BETTER_AUTH_SECRET set

## Implementation Roadmap

### Phase 1: Integrate Authentication into Task Router

File: backend/src/api/routers/tasks.py

Key changes:
1. Add import: from backend.auth import UserIdentity, get_current_user
2. Update all endpoint signatures to include current_user dependency
3. Remove user_id path parameter
4. Add current_user: Annotated[UserIdentity, Depends(get_current_user)]
5. Use current_user.id instead of URL parameter
6. Update route paths to /tasks (no user_id prefix)

Apply to all 6 endpoints:
- POST /tasks (create)
- GET /tasks (list)
- GET /tasks/{task_id} (get)
- PUT /tasks/{task_id} (update)
- DELETE /tasks/{task_id} (delete)
- PATCH /tasks/{task_id}/complete (mark complete)

### Phase 2: Update Task Service Layer

File: backend/src/services/task_service.py

Goal: All queries filtered by user_id

Pattern: Add WHERE (condition) & (Task.user_id == user_id) to all select statements

Apply filter pattern to all methods:
- get_task(task_id, user_id) → WHERE id = ? AND user_id = ?
- get_tasks(user_id, skip, limit) → WHERE user_id = ?
- update_task(task_id, user_id, data) → WHERE id = ? AND user_id = ?
- delete_task(task_id, user_id) → WHERE id = ? AND user_id = ?
- mark_complete(task_id, user_id) → WHERE id = ? AND user_id = ?

### Phase 3: Test Implementation

File: backend/tests/test_user_isolation.py (NEW)

Create tests for:
- Missing Authorization header returns 401
- Expired JWT returns 401
- Invalid signature returns 401
- User B cannot see User A's tasks (returns 404)
- User B cannot delete User A's task (returns 404)

File: backend/tests/integration/test_api_security.py (NEW)

Create end-to-end tests validating full request/response cycles

Run tests:
cd backend
python -m pytest tests/test_user_isolation.py tests/integration/test_api_security.py -v

## Environment Configuration

File: .env

BETTER_AUTH_SECRET=your-shared-secret-here-min-32-chars
DATABASE_URL=postgresql+asyncpg://user:password@localhost/tododb
PROJECT_NAME=Todo App
API_V1_STR=/api

## Validation Checklist

- All task endpoints require Authorization header
- Missing Authorization header returns 401
- Expired JWT returns 401
- Invalid signature returns 401
- Valid JWT returns 200 with user's tasks only
- User A cannot GET User B's task (returns 404)
- User A cannot DELETE User B's task (returns 404)
- Task creation assigns user_id from JWT, not request body
- All database queries include WHERE user_id = ? filter
- Health check endpoint remains unprotected

## API Usage Examples

### Create Task with Valid Token

curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'

Response: 201 Created with task details

### List Tasks

curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

Response: 200 OK with array of tasks

### Missing Token

curl http://localhost:8000/api/tasks

Response: 401 Unauthorized

## References

- JWT Specification: RFC 7519
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- OpenAPI Spec: specs/002-auth-api-security/contracts/openapi.yaml
