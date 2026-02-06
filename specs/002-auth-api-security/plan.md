# Implementation Plan: Authentication & API Security

**Branch**: `002-auth-api-security` | **Date**: 2026-01-10 | **Spec**: `/specs/002-auth-api-security/spec.md`
**Input**: Feature specification from `/specs/002-auth-api-security/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Enable stateless, secure JWT-based API authentication across all FastAPI endpoints. The backend already has JWT verification logic implemented (`backend/auth.py`). This plan focuses on:
1. Integrating JWT verification middleware into all task endpoints
2. Extracting user identity from JWT and enforcing task ownership
3. Ensuring 100% multi-user data isolation
4. Validating security behavior with comprehensive test coverage

The technical approach is straightforward: middleware validates tokens, extracts user_id from JWT claims, and all database queries filter by authenticated user to prevent cross-user access.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, PyJWT, python-dotenv
**Storage**: Neon Serverless PostgreSQL (persistent)
**Testing**: pytest, httpx (async HTTP client for testing)
**Target Platform**: Linux server (cloud-deployed)
**Project Type**: Web application (backend component)
**Performance Goals**: < 50ms token verification overhead per request
**Constraints**: Stateless JWT verification; no session storage; HMAC-SHA256 signature validation
**Scale/Scope**: Multi-user todo app; initial support for 100+ concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **1. Spec-Driven Development Compliance**: All implementation is directly derived from `/specs/002-auth-api-security/spec.md` requirements (FR-001 through FR-006). No manual coding without spec updates.

✅ **2. Correctness & Security**: Security-by-design enforced via:
   - Mandatory JWT verification on every endpoint
   - User isolation at the database query level (all queries filtered by authenticated user_id)
   - Stateless token validation (no server-side session storage)
   - User identity extracted from JWT claims, not URL parameters

✅ **3. Separation of Concerns**:
   - Frontend: Manages login flow and token storage (via Better Auth)
   - Backend (FastAPI): Enforces JWT validation and task ownership filtering
   - Auth (Better Auth): Handles user signup/signin and token issuance
   - Data (Neon Postgres): Stores tasks with user_id foreign key relationship

✅ **4. Production-Grade**: Architecture supports real users:
   - Persistent storage in Neon Serverless PostgreSQL
   - Proper error handling (401 for invalid/missing tokens, 404 for non-existent tasks)
   - Async/await pattern for performance and scalability
   - No in-memory or mock storage

✅ **5. Test-First Approach**: Comprehensive test coverage required (valid tokens, invalid tokens, expired tokens, multi-user isolation)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── routers/
│   │       └── tasks.py (MODIFY: Add get_current_user dependency to all endpoints)
│   ├── core/
│   │   ├── config.py (VERIFY: BETTER_AUTH_SECRET env var present)
│   │   └── db.py (async session management)
│   ├── models/
│   │   └── task.py (Task model with user_id field)
│   ├── services/
│   │   └── task_service.py (MODIFY: Filter queries by user_id)
│   └── main.py (FastAPI app setup)
├── auth.py (EXISTING: JWT verification logic - no changes needed)
├── tests/
│   ├── test_auth.py (MODIFY: Add comprehensive JWT validation tests)
│   ├── test_user_isolation.py (NEW: Multi-user data isolation tests)
│   └── integration/
│       └── test_api_security.py (NEW: End-to-end security tests)
└── pytest.ini
```

**Structure Decision**: Web application with backend component. The existing `backend/` structure supports authentication & security needs. Key modifications:
1. Task router endpoints depend on `get_current_user` to verify JWT
2. Task service filters all queries by authenticated user_id
3. Task creation overrides any client-provided user_id with authenticated user_id
4. Comprehensive security tests validate token handling and multi-user isolation

## Complexity Tracking

**No Constitution violations detected.** All requirements align with established principles:
- JWT verification is simpler and more secure than session storage
- Filtering at the database layer ensures no architectural workarounds
- Existing FastAPI middleware patterns support seamless integration
- No additional complexity layers needed beyond core auth + isolation

---

## Phase 0: Research Complete ✅

**Output**: `research.md`

**Key Decisions Locked In**:
1. JWT verification with HMAC-SHA256 (already implemented in `backend/auth.py`)
2. FastAPI dependency injection for per-endpoint authentication
3. User identity extracted from JWT "sub" claim (JWT-only source of truth)
4. Database query filtering at service layer (defense in depth)
5. 401 for auth failures, 404 for non-existent resources (security by obscurity)
6. Environment-based secret rotation with container restart
7. Three-layer test suite (unit, integration, E2E)

**Next**: Phase 1 design

---

## Phase 1: Design & Contracts Complete ✅

**Outputs**:
- `data-model.md` - Entity relationships, validation rules, multi-user isolation guarantees
- `contracts/openapi.yaml` - OpenAPI 3.0 specification for all endpoints
- `contracts/auth-contract.md` - Authentication flow, error handling, security patterns
- `quickstart.md` - Implementation roadmap and code examples

### Data Model Highlights

| Entity | Storage | Isolation |
|--------|---------|-----------|
| UserIdentity | In-memory (JWT claims) | Stateless; not persisted |
| Task | PostgreSQL | user_id indexed; all queries filtered |

### API Contract Summary

**Authentication**: All endpoints require `Authorization: Bearer <JWT>` header

**Endpoints**:
- POST /api/tasks - Create task (user_id from JWT)
- GET /api/tasks - List user's tasks
- GET /api/tasks/{task_id} - Get single task (404 if not owned)
- PUT /api/tasks/{task_id} - Update task (404 if not owned)
- DELETE /api/tasks/{task_id} - Delete task (404 if not owned)
- PATCH /api/tasks/{task_id}/complete - Mark complete (404 if not owned)

**Error Codes**:
- 401 Unauthorized - Missing/invalid/expired token
- 404 Not Found - Task not found OR not owned (indistinguishable)
- 201 Created - Task created successfully

### Test Strategy

**Unit Tests** (`test_auth.py`):
- Valid token verification
- Expired token rejection
- Invalid signature rejection
- Missing "sub" claim rejection

**Integration Tests** (`test_user_isolation.py`):
- Multi-user isolation
- Cross-user access prevention
- Task ownership enforcement

**E2E Tests** (`integration/test_api_security.py`):
- Full request/response cycles
- Valid token workflow
- Invalid token rejection

---

## Next: Phase 2 (Tasks Generation)

The `/sp.tasks` command will generate `tasks.md` with:
- Granular implementation tasks for each endpoint
- Task ownership validation logic
- Test case specifications
- Deployment checklist

This plan is **COMPLETE and APPROVED** for implementation.
