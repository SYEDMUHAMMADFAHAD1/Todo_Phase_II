---
description: "Task list for Authentication & API Security feature implementation"
---

# Tasks: Authentication & API Security

**Input**: Design documents from `/specs/002-auth-api-security/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md
**Constitution Compliance**: All tasks follow Spec-Driven Development, Security-by-Design, and Correctness-First principles

**Feature Branch**: `002-auth-api-security` | **Target**: Backend API authentication & multi-user data isolation

**Tests**: Tests are MANDATORY (TDD approach) - write before implementation, expect failures initially

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/`
- **Specs**: `specs/002-auth-api-security/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Install PyJWT and cryptography dependencies in backend/requirements.txt
- [ ] T002 [P] Create initial auth module structure in backend/auth.py
- [ ] T003 [P] Add BETTER_AUTH_SECRET to .env.example (do not commit actual secrets)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Implement JWT verification logic using PyJWT in backend/auth.py
- [ ] T005 Create get_current_user dependency in backend/auth.py to fail on missing/invalid tokens
- [ ] T006 Update backend/models.py to ensure strictly typed user_id fields
- [ ] T007 [P] Create unit tests for JWT verification in backend/tests/test_auth.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Secure API Access (Priority: P1) 🎯 MVP

**Goal**: Block unauthenticated requests so that task data remains private

**Independent Test**: Can be fully tested using standard HTTP clients by sending requests with valid, invalid, and missing tokens via curl/pytest

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T008 [P] [US1] Create test case for missing Authorization header in backend/tests/test_auth_integration.py
- [ ] T009 [P] [US1] Create test case for invalid/expired tokens in backend/tests/test_auth_integration.py

### Implementation for User Story 1

- [ ] T010 [US1] Apply get_current_user dependency to all protected routes in backend/routers/tasks.py
- [ ] T011 [US1] Implement 401 Unauthorized handling in backend/main.py exception handlers
- [ ] T012 [US1] Verify Swagger UI authorize button configuration in backend/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Isolation (Priority: P1)

**Goal**: Ensure users see only their own tasks so that my todo list is not cluttered or exposed to others

**Independent Test**: Create two users (A and B), perform operations as User A, and verify User B cannot see or modify User A's data

### Tests for User Story 2 ⚠️

- [ ] T013 [P] [US2] Create multi-user isolation test in backend/tests/test_isolation.py (User A vs User B)

### Implementation for User Story 2

- [ ] T014 [US2] Update GET /tasks endpoint to filter by current_user.id in backend/routers/tasks.py
- [ ] T015 [US2] Update POST /tasks to strictly assign current_user.id (ignoring body input) in backend/routers/tasks.py
- [ ] T016 [US2] Update PUT/DELETE endpoints to enforce ownership checks (and return 404) in backend/routers/tasks.py
- [ ] T017 [US2] Verify data persistence ensures user_id integrity in backend/database.py (if manual SQL involved)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T018 [P] Update API documentation (OpenAPI) description for security schemes
- [ ] T019 Run full security regression test suite
- [ ] T020 [P] Document environment configuration for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (Secure API) is the MVP
  - User Story 2 (Isolation) builds on the secured endpoints

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P1)**: Depends on User Story 1 (Secured endpoints needed to test isolation)

### Parallel Opportunities

- T008 and T009 (US1 Tests) can run in parallel
- T010 and T011 (Auth integration) can run in parallel
- T013 (US2 Test) is independent of implementation

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (Auth Middleware)
3. Complete Phase 3: User Story 1 (Block unauthenticated traffic)
4. **STOP and VALIDATE**: Verify 401s for invalid requests
5. Deploy/demo auth blockage

### Incremental Delivery

1. **Secure Barrier**: First ensure no one gets in without a key (US1)
2. **Data Silos**: Then ensure logged-in users only see their own room (US2)
