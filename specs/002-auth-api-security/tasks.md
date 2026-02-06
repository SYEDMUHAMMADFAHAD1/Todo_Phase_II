---
description: "Task list for Authentication & API Security feature implementation"
---

# Tasks: Authentication & API Security

**Input**: Design documents from `/specs/002-auth-api-security/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md
**Constitution Compliance**: All tasks follow Spec-Driven Development, Security-by-Design, and Correctness-First principles

**Feature Branch**: `002-auth-api-security` | **Target**: Backend API authentication & multi-user data isolation

**Tests**: Tests are MANDATORY (TDD approach) - write before implementation, expect failures initially

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- **Description**: Clear action with exact file paths

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify prerequisites and establish testing framework

- [ ] T001 Verify .env file has BETTER_AUTH_SECRET set; document in backend/.env.example
- [ ] T002 Install test dependencies: pytest, httpx, pytest-asyncio
- [ ] T003 [P] Review backend/auth.py JWT verification implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure MUST complete before user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Verify backend/src/core/config.py loads BETTER_AUTH_SECRET from environment with validation
- [ ] T005 Verify backend/src/core/db.py async session management works correctly
- [ ] T006 Verify backend/src/models/task.py has user_id field (indexed) and all required fields
- [ ] T007 [P] Create test fixtures in backend/tests/conftest.py:
  - create_valid_jwt(user_id), create_expired_jwt(user_id), create_invalid_signature_jwt()
- [ ] T008 [P] Create async test client helper in backend/tests/conftest.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Secure API Access (Priority: P1) 🎯 MVP

**Goal**: Backend blocks unauthenticated requests and validates JWT tokens on all endpoints

**Independent Test**: Test endpoints with valid, invalid, expired, and missing tokens

### Tests for User Story 1

- [ ] T009 [P] [US1] Create backend/tests/test_auth_validation.py:
  - Valid JWT passes verification
  - Expired JWT rejected with 401
  - Invalid signature rejected with 401
  - Missing Authorization header returns 401
  - Malformed Bearer header returns 401
  - UserIdentity extracts id, email, name from JWT

- [ ] T010 [P] [US1] Create backend/tests/contract/test_task_endpoints_auth.py:
  - All 6 endpoints without Authorization → 401 Unauthorized
  - Valid JWT on GET /api/tasks → 200 OK

### Implementation for User Story 1

- [ ] T011 [US1] Add imports to backend/src/api/routers/tasks.py:
  - from typing import Annotated
  - from backend.auth import UserIdentity, get_current_user
  - from fastapi import status

- [ ] T012 [US1] Update POST /api/tasks in backend/src/api/routers/tasks.py:
  - Remove user_id path parameter
  - Add current_user: Annotated[UserIdentity, Depends(get_current_user)]
  - Route: "/{user_id}/tasks" → "/tasks"
  - Status: 201 Created

- [ ] T013 [US1] Update GET /api/tasks in backend/src/api/routers/tasks.py:
  - Remove user_id path parameter
  - Add current_user dependency
  - Route: "/{user_id}/tasks" → "/tasks"
  - Keep skip/limit parameters

- [ ] T014 [US1] Update GET /api/tasks/{task_id} in backend/src/api/routers/tasks.py:
  - Remove user_id path parameter
  - Add current_user dependency
  - Route: "/{user_id}/tasks/{task_id}" → "/tasks/{task_id}"

- [ ] T015 [US1] Update PUT /api/tasks/{task_id} in backend/src/api/routers/tasks.py:
  - Remove user_id path parameter
  - Add current_user dependency
  - Route: "/{user_id}/tasks/{task_id}" → "/tasks/{task_id}"

- [ ] T016 [US1] Update DELETE /api/tasks/{task_id} in backend/src/api/routers/tasks.py:
  - Remove user_id path parameter
  - Add current_user dependency
  - Route: "/{user_id}/tasks/{task_id}" → "/tasks/{task_id}"
  - Status: 204 No Content

- [ ] T017 [US1] Update PATCH /api/tasks/{task_id}/complete in backend/src/api/routers/tasks.py:
  - Remove user_id path parameter
  - Add current_user dependency
  - Route: "/{user_id}/tasks/{task_id}/complete" → "/tasks/{task_id}/complete"

- [ ] T018 [US1] Add documentation to backend/src/api/routers/tasks.py:
  - Docstrings explaining authentication requirement
  - 401 response documentation for all endpoints

**Checkpoint**: US1 complete - all endpoints require valid JWT; unauthenticated requests rejected with 401

---

## Phase 4: User Story 2 - User Isolation (Priority: P1)

**Goal**: Users access only their own tasks; multi-user data isolation at service and database layers

**Independent Test**: Create users A and B; verify B cannot see/modify A's tasks; verify task ownership from JWT

### Tests for User Story 2

- [ ] T019 [P] [US2] Create backend/tests/integration/test_user_isolation.py:
  - User A creates task; GET returns 1 task for A
  - User B GET returns empty list
  - User B GET other's task_id returns 404
  - User B DELETE other's task returns 404
  - Task user_id matches authenticated user, ignoring request body

- [ ] T020 [P] [US2] Create backend/tests/test_task_ownership.py:
  - POST with user_id in body → task saved with JWT user_id
  - Task update only succeeds if user_id matches JWT
  - Task deletion only succeeds if user_id matches JWT

### Implementation for User Story 2

- [ ] T021 [US2] Update TaskService.get_task() in backend/src/services/task_service.py:
  - Add filter: WHERE id = ? AND user_id = ?
  - Return None if not found OR user_id mismatch

- [ ] T022 [US2] Update TaskService.get_tasks() in backend/src/services/task_service.py:
  - Add filter: WHERE user_id = ?
  - Only return user's tasks

- [ ] T023 [US2] Update TaskService.update_task() in backend/src/services/task_service.py:
  - Add filter: WHERE id = ? AND user_id = ?
  - Return None if not found OR mismatch

- [ ] T024 [US2] Update TaskService.delete_task() in backend/src/services/task_service.py:
  - Add filter: WHERE id = ? AND user_id = ?
  - Return False if not found OR mismatch

- [ ] T025 [US2] Update TaskService.mark_complete() in backend/src/services/task_service.py:
  - Add filter: WHERE id = ? AND user_id = ?
  - Return None if not found OR mismatch

- [ ] T026 [US2] Update TaskService.create_task() in backend/src/services/task_service.py:
  - Use user_id parameter (from authenticated user)
  - Assign user_id to task before saving
  - Verify correct user_id in database

- [ ] T027 [P] [US2] Add logging to backend/src/services/task_service.py:
  - Log user_id filtering in all query methods
  - Log task ownership assignment in create_task

**Checkpoint**: US2 complete - strict user isolation; users access only their own tasks

---

## Phase 5: Validation & Security Verification

**Purpose**: Comprehensive test coverage and security validation

- [ ] T028 [P] Run unit tests: pytest backend/tests/test_auth.py backend/tests/test_auth_validation.py -v
- [ ] T029 [P] Run contract tests: pytest backend/tests/contract/test_task_endpoints_auth.py -v
- [ ] T030 [P] Run integration tests: pytest backend/tests/integration/ backend/tests/test_task_ownership.py -v
- [ ] T031 Run full test suite with coverage: pytest backend/tests/ --cov=backend/src --cov-report=term-missing
  - Target: ≥80% coverage for auth and service layers
  - Document: backend/COVERAGE.md

- [ ] T032 [US1] Verify SC-001: Confirm 401 Unauthorized for missing/invalid/expired tokens
- [ ] T033 [US2] Verify SC-002: Confirm 0% cross-user data leakage
- [ ] T034 [P] Verify SC-003: Measure token verification latency
  - Profile: 100 requests with valid token
  - Target: All < 50ms
  - Document: backend/PERFORMANCE.md

- [ ] T035 [US1] Verify SC-004: JWT verification adheres to Better Auth standard
  - Algorithm: HMAC-SHA256 ✓
  - Claims: sub, exp, iat ✓
  - Signature: BETTER_AUTH_SECRET ✓

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories

- [ ] T036 [P] Add error handling logging in backend/src/api/routers/tasks.py:
  - Log 401 and 404 responses with context
  - Use structured logging

- [ ] T037 [P] Update backend/README.md:
  - Add "Authentication & Security" section
  - Describe JWT flow
  - Explain user isolation
  - Add request examples

- [ ] T038 Update backend/README.md setup instructions:
  - BETTER_AUTH_SECRET required in .env
  - DATABASE_URL required
  - Example values

- [ ] T039 [P] Run code quality checks:
  - black backend/src --check
  - mypy backend/src (if configured)
  - pylint backend/src (if configured)

- [ ] T040 Create backend/SECURITY_TESTING.md:
  - Tamper with JWT → rejected
  - Expired token → 401
  - Wrong secret → rejected
  - Cross-user access → 404
  - Privilege escalation attempt → overridden

- [ ] T041 Validate quickstart.md:
  - Follow specs/002-auth-api-security/quickstart.md
  - Verify all steps complete
  - Test code examples
  - Document: QUICKSTART_VALIDATION.md

- [ ] T042 Final integration test:
  - Start: python -m uvicorn backend.src.main:app --reload
  - Valid token: GET /api/tasks → user's tasks
  - Invalid token: → 401 Unauthorized
  - Multi-user: Create 2 users, verify isolation
  - Document: INTEGRATION_TEST_RESULTS.md

---

## Dependencies & Execution Order

### Phase Dependencies
- Phase 1: No dependencies
- Phase 2: Depends on Phase 1 - BLOCKS all user stories
- Phase 3: Depends on Phase 2
- Phase 4: Depends on Phase 2 (can overlap with Phase 3)
- Phase 5: Depends on Phases 3 & 4
- Phase 6: Depends on all phases

### Parallel Opportunities
- Phase 2: T007, T008 can run in parallel
- Phase 3: T009, T010 can run in parallel; T012-T017 can run in parallel
- Phase 4: T019, T020 can run in parallel; T021-T026 can run in parallel
- Phase 5: T028-T030, T034-T035 can run in parallel
- Phase 6: All [P] tasks can run in parallel

### MVP Strategy
Stop after Phase 4 for full feature:
1. Phase 1: Setup ✓
2. Phase 2: Foundational ✓
3. Phase 3: US1 (Secure API Access) ✓
4. Phase 4: US2 (User Isolation) ✓
5. Run Phase 5 validation → All tests PASS → Production-ready

---

## Constitution Compliance

All tasks follow project principles:
1. **Spec-Driven**: Tasks reference spec.md requirements (FR-001 through FR-006)
2. **Security-by-Design**: Tasks T019-T027 enforce multi-user isolation
3. **Test-First**: Tests defined before implementation
4. **Correctness-First**: All endpoints validated for proper responses
5. **Clean Code**: Logging, error handling, documentation

---

## Success Criteria

✅ Phase 3 complete: US1
- All 6 endpoints require Authorization header
- Missing/Invalid/Expired token → 401 Unauthorized
- Valid token → 200 OK

✅ Phase 4 complete: US2
- User A cannot see/modify User B's tasks
- Task user_id from JWT, not request body
- All queries filtered by user_id

✅ Phase 5 complete: Validation
- Coverage ≥ 80%
- Token latency < 50ms
- SC-001 through SC-004 verified

✅ Phase 6 complete: Production-Ready
- Code formatted, linted, documented
- Security testing guide complete
- Integration results documented
