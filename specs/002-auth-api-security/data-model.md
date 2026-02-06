# Phase 1 Data Model: Authentication & API Security

**Date**: 2026-01-10 | **Branch**: `002-auth-api-security` | **Status**: Complete

## Entity Diagram

```
┌─────────────────────────────────────┐
│         Better Auth (External)      │
│  ├─ User ID (JWT 'sub' claim)       │
│  ├─ Email                           │
│  └─ Name                            │
└────────────────┬────────────────────┘
                 │ (stateless trust)
                 │ JWT verification
                 │
┌────────────────▼────────────────────┐
│      FastAPI UserIdentity            │
│  ├─ id: str (from JWT 'sub')        │
│  ├─ email: Optional[str]            │
│  └─ name: Optional[str]             │
└────────────────┬────────────────────┘
                 │ (dependency injection)
                 │
┌────────────────▼────────────────────┐
│           Task (PostgreSQL)          │
│  ├─ id: UUID (primary key)          │
│  ├─ user_id: str (indexed, FK)      │
│  ├─ title: str (max 255 chars)      │
│  ├─ description: Optional[str]      │
│  ├─ is_completed: bool              │
│  ├─ created_at: datetime            │
│  └─ updated_at: datetime            │
└─────────────────────────────────────┘
```

## Data Model Specification

### UserIdentity (Pydantic Model - In-Memory)

**Location**: `backend/auth.py:20-27`

| Field | Type | Constraints | Notes |
|-------|------|-----------|-------|
| id | str | Non-empty | Extracted from JWT "sub" claim; identifies user across system |
| email | Optional[str] | None or email format | From JWT "email" claim; may be None |
| name | Optional[str] | None or string | From JWT "name" claim; for display purposes |

**Validation Rules**:
- `id` is mandatory and non-empty (enforced by JWT verification)
- `email` and `name` are optional; missing from JWT treated as None

**Lifecycle**:
- Created fresh on every authenticated request
- Extracted from JWT; NOT stored in database
- Discarded after request completes

---

### Task (SQLModel - Persisted)

**Location**: `backend/src/models/task.py:9-14`

| Field | Type | Constraints | Indexed | Notes |
|-------|------|-----------|---------|-------|
| id | UUID | Auto-generated | Primary Key | Created on insert; immutable |
| user_id | str | Non-empty | Yes | **CRITICAL**: Foreign key to user from JWT; filters all queries |
| title | str | Max 255 chars | No | Task title; required on creation |
| description | Optional[str] | None or text | No | Optional task details |
| is_completed | bool | Default False | No | Completion status; mutable by owner only |
| created_at | datetime | UTC timestamp | No | Set at creation; never modified |
| updated_at | datetime | UTC timestamp | No | Updated on every modification |

**Validation Rules**:
- `title` is mandatory (enforced at schema level in TaskCreate)
- `user_id` is immutable after creation (assigned from authenticated user)
- `is_completed` defaults to False
- `created_at` and `updated_at` are system-managed

**Relationships**:
- **Implicit**: user_id references user in Better Auth (not enforced via FK due to external auth system)
- **Query Pattern**: ALL queries must include `WHERE user_id = :authenticated_user_id`

**Indexes**:
- `user_id` (single-column): Enables fast filtering of user's tasks
- `id` (primary key): Default

**Expected Query Patterns**:
1. List all tasks for user_id → `SELECT * FROM task WHERE user_id = ? ORDER BY created_at`
2. Get single task by id and user_id → `SELECT * FROM task WHERE id = ? AND user_id = ?`
3. Create task for user_id → `INSERT INTO task (..., user_id, ...) VALUES (..., ?, ...)`
4. Update task if owner → `UPDATE task SET ... WHERE id = ? AND user_id = ?`
5. Delete task if owner → `DELETE FROM task WHERE id = ? AND user_id = ?`

---

## Multi-User Isolation Guarantees

### Isolation Mechanism

**Layer 1 - Authentication**: JWT verification (`backend/auth.py:34-72`)
- Validates token signature against BETTER_AUTH_SECRET
- Extracts authenticated user_id from "sub" claim
- Returns 401 Unauthorized if invalid/expired/missing

**Layer 2 - Authorization**: Task ownership enforcement (`backend/src/services/task_service.py`)
- Every database query includes `WHERE user_id = :authenticated_user_id` filter
- Service methods receive user_id parameter; filter by it before returning data
- No cross-user reads, writes, or deletes possible

**Layer 3 - API Routes**: Endpoint protection (`backend/src/api/routers/tasks.py`)
- All task endpoints require `current_user: Annotated[UserIdentity, Depends(get_current_user)]`
- Route parameter `user_id` is NOT trusted; uses authenticated `current_user.id` instead
- 404 Not Found returned for non-existent OR non-owned tasks (indistinguishable to client)

### Isolation Test Cases

| Scenario | Input | Expected Behavior | HTTP Status |
|----------|-------|-------------------|-------------|
| User A lists tasks | JWT for A | Returns only A's tasks | 200 |
| User B lists tasks | JWT for B | Returns only B's tasks (empty if none) | 200 |
| User B attempts GET User A's task | URL has A's task_id, JWT for B | Not found | 404 |
| User B attempts DELETE User A's task | URL has A's task_id, JWT for B | Not deleted; 404 response | 404 |
| User A creates task, provides user_id=B | JWT for A, body.user_id=B | Task saved with user_id=A | 201 |
| Request without Authorization header | GET /tasks, no header | Unauthorized | 401 |
| Request with expired JWT | Valid format, expired exp claim | Unauthorized | 401 |
| Request with invalid signature | Valid JWT format, wrong secret | Unauthorized | 401 |

---

## Schema Evolution Notes

**Current Phase**: Initial implementation (Spec 2 - Authentication & API Security)

**Considerations for Future Phases**:
- If shared tasks (multi-user ownership) required → add `task_collaborators` junction table
- If task history/audit logging needed → add `task_events` table with user_id and timestamp
- If soft-delete required → add `deleted_at` nullable timestamp to Task
- Existing `owner_id` field (legacy) should be removed once migration complete

**No Breaking Changes Expected** for Spec 2 implementation.

---

## Database Migration Notes

**New Tables**: None (Task table already exists from Spec 1)

**New Columns**: None (user_id already indexed from Spec 1)

**Index Creation**:
```sql
CREATE INDEX IF NOT EXISTS idx_task_user_id ON task(user_id);
```

**Existing Indexes**:
- `idx_task_user_id` already present in migration `2a0b93aa388b_create_task_table.py`

**No data migration required** - user_id column pre-populated in Spec 1.
