# Authentication Contract

**Date**: 2026-01-10 | **Feature**: Authentication & API Security | **Version**: 1.0

## Overview

This document defines the authentication contract between the frontend (Better Auth) and backend (FastAPI). All task endpoints require valid JWT tokens in the Authorization header.

## Token Issuance (Frontend Responsibility)

**Source**: Better Auth (external authentication service)

**Token Format**: JWT (JSON Web Token)

### JWT Structure

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyLWlkLXVybiIsImVtYWlsIjoiamFrZUBleGFtcGxlLmNvbSIsIm5hbWUiOiJKYWtlIiwiaWF0IjoxNjM2MzM2MDAwLCJleHAiOjE2MzYzMzk2MDB9.signature
```

### Required Claims

| Claim | Type | Required | Example | Notes |
|-------|------|----------|---------|-------|
| sub | string | Yes | "user-id-urn" | Subject (user ID); uniquely identifies user; extracted into UserIdentity.id |
| iat | number | Yes | 1636336000 | Issued at (Unix timestamp) |
| exp | number | Yes | 1636339600 | Expiration (Unix timestamp); PyJWT validates automatically |

### Optional Claims

| Claim | Type | Optional | Example | Notes |
|-------|------|----------|---------|-------|
| email | string | Yes | "jake@example.com" | User email; extracted into UserIdentity.email |
| name | string | Yes | "Jake" | User display name; extracted into UserIdentity.name |

### Token Signing

- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret**: `BETTER_AUTH_SECRET` (shared between Better Auth and FastAPI backend)
- **Key Storage**: 
  - Better Auth: Internal secret management
  - FastAPI: Environment variable `.env` file (development) or container secrets (production)

## Token Verification (Backend Responsibility)

**Location**: `backend/auth.py`

### Verification Flow

```
1. Client sends HTTP request with Authorization header
   Authorization: Bearer eyJhbGc...

2. FastAPI security dependency extracts bearer token
   HTTPAuthorizationCredentials.credentials = "eyJhbGc..."

3. get_current_user() calls verify_token(token)
   - Validates signature against BETTER_AUTH_SECRET
   - Checks expiration (PyJWT raises ExpiredSignatureError if expired)
   - Returns decoded payload or raises AuthError

4. UserIdentity created from payload claims
   UserIdentity(
     id=payload["sub"],
     email=payload.get("email"),
     name=payload.get("name")
   )

5. Endpoint handler receives current_user: UserIdentity
   - Can access current_user.id for filtering queries
   - All database operations filtered by this user_id
```

### Error Handling

| Scenario | Exception | HTTP Response | WWW-Authenticate Header |
|----------|-----------|---------------|----------------------|
| Missing Authorization header | No credentials | 401 Unauthorized | Bearer |
| Malformed header (missing "Bearer ") | Invalid credentials | 401 Unauthorized | Bearer |
| Expired token | jwt.ExpiredSignatureError | 401 Unauthorized | Bearer |
| Invalid signature | jwt.InvalidTokenError | 401 Unauthorized | Bearer |
| Missing "sub" claim | Missing subject | 401 Unauthorized | Bearer |
| Missing BETTER_AUTH_SECRET | Server config error | 500 Internal Server Error | (none) |

### Success Response

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "user-123",
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "created_at": "2026-01-10T10:30:00Z",
  "updated_at": "2026-01-10T10:30:00Z"
}
```

## API Request Format

### Valid Request

```http
GET /api/tasks HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

### Invalid Requests

**Missing Authorization header**:
```http
GET /api/tasks HTTP/1.1
Host: localhost:8000
```
→ 401 Unauthorized

**Invalid Bearer format**:
```http
GET /api/tasks HTTP/1.1
Authorization: Basic dXNlcjpwYXNz
```
→ 401 Unauthorized (only Bearer scheme accepted)

**Expired token**:
```http
GET /api/tasks HTTP/1.1
Authorization: Bearer eyJhbGc...exp-claim-in-past...
```
→ 401 Unauthorized

## Task Creation: User Assignment

### Specification

When creating a task, the authenticated user_id is **always** assigned, regardless of request body:

```http
POST /api/tasks HTTP/1.1
Authorization: Bearer eyJh...sub:"user-alice"...
Content-Type: application/json

{
  "title": "Buy milk",
  "user_id": "user-bob"  # This is IGNORED
}
```

**Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-alice",  # Assigned from JWT, not request body
  "title": "Buy milk",
  "is_completed": false,
  "created_at": "2026-01-10T12:00:00Z",
  "updated_at": "2026-01-10T12:00:00Z"
}
```

### Implementation

```python
@router.post("/tasks", response_model=TaskRead)
async def create_task(
    task_in: TaskCreate,
    current_user: Annotated[UserIdentity, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    # current_user.id is from JWT; used for all operations
    return await service.create_task(task_in, current_user.id)
```

## Multi-User Data Isolation

### Principle

Every database query is filtered by authenticated `user_id`. Clients cannot access or modify data belonging to other users.

### Query Pattern

All TaskService methods receive `user_id: str` parameter:

```python
async def get_tasks(self, user_id: str, skip: int = 0, limit: int = 100):
    statement = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
    result = await self.session.execute(statement)
    return result.scalars().all()
```

### Test Case: Cross-User Access Attempt

```python
# User Alice tries to delete User Bob's task
DELETE /api/tasks/bob-task-uuid
Authorization: Bearer eyJh...sub:"user-alice"...

# Response: 404 Not Found
{
  "detail": "Task not found"
}

# Backend logic:
# 1. Verify JWT → user_id = "user-alice"
# 2. Query: SELECT * FROM task WHERE id = ? AND user_id = ?
#    Parameters: [bob-task-uuid, user-alice]
# 3. No row found → return 404 (not 403, to hide task ownership)
```

## Secret Rotation

### Current Approach

Environment-based rotation:

1. Update `.env` or container secret with new `BETTER_AUTH_SECRET`
2. Restart FastAPI application
3. New tokens validated with new secret; old tokens invalid (exp check fails after rotation)

### Future Consideration

If zero-downtime rotation needed: Implement dual-key validation (old + new secret simultaneously for grace period).

## Backward Compatibility

**Breaking Change**: Once deployed, all endpoints require valid JWT. No fallback to unauthenticated access.

**Health Check Exception**: `/health` endpoint remains unprotected for load balancer probes.

## Testing

See `backend/tests/test_auth.py` and `backend/tests/integration/test_api_security.py` for test cases covering:
- Valid token → 200 OK
- Missing token → 401 Unauthorized
- Expired token → 401 Unauthorized
- Invalid signature → 401 Unauthorized
- Multi-user isolation → 404 Not Found
