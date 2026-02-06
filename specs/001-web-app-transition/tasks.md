# Implementation Tasks: Web App Transition (Spec 1: Backend Core)

**Branch**: `001-web-app-transition` | **Spec**: [specs/001-web-app-transition/spec.md](./spec.md)
**Plan**: [specs/001-web-app-transition/plan.md](./plan.md)

## Phase 1: Project Setup (Backend Initialization)

> **Goal**: Initialize the FastAPI backend project structure and database connection.

- [x] T001 Initialize FastAPI project structure with strict modular separation in `backend/`
  - Create `backend/src/api/routers/`, `backend/src/services/`, `backend/src/models/`, `backend/src/core/`
- [x] T002 Configure Environment and Database Settings in `backend/src/core/config.py`
- [x] T003 Configure Async Database Engine and Session Dependency in `backend/src/core/db.py`
- [x] T004 Initialize Alembic for database migrations in `backend/`

## Phase 2: Data Layer Foundation

> **Goal**: Define the data model and applying the schema to Neon PostgreSQL.

- [x] T005 [US2] Define `Task` SQLModel entity with `owner_id` field in `backend/src/models/task.py`
  - Fields: `id`, `title`, `description`, `completed`, `created_at`, `updated_at`, `owner_id`
- [x] T006 [US2] Create and Apply Alembic migration for `task` table

## Phase 3: Task Management API Implementation (User Story 2)

> **Goal**: Implement complete CRUD functionality for Tasks (Spec 1 Pre-Auth Mode).
> **Note**: `user_id` is passed via path parameter for Spec 1 validation.

### Service Layer
- [x] T007 [US2] Implement `TaskService` with CRUD logic in `backend/src/services/task_service.py`
  - Methods: `create_task`, `get_tasks`, `get_task`, `update_task`, `delete_task`

### API Layer
- [x] T008 [P] [US2] Implement `POST /api/{user_id}/tasks` endpoint in `backend/src/api/routers/tasks.py`
- [x] T009 [P] [US2] Implement `GET /api/{user_id}/tasks` endpoint in `backend/src/api/routers/tasks.py`
- [x] T010 [P] [US2] Implement `GET /api/{user_id}/tasks/{task_id}` endpoint in `backend/src/api/routers/tasks.py`
- [x] T011 [P] [US2] Implement `PUT /api/{user_id}/tasks/{task_id}` endpoint in `backend/src/api/routers/tasks.py`
- [x] T012 [P] [US2] Implement `DELETE /api/{user_id}/tasks/{task_id}` endpoint in `backend/src/api/routers/tasks.py`
- [x] T013 [P] [US2] Implement `PATCH /api/{user_id}/tasks/{task_id}/complete` endpoint in `backend/src/api/routers/tasks.py`
- [x] T014 [US2] Register task router in `backend/src/main.py`

## Phase 4: Validation & Quality

> **Goal**: Verify correctness and persistence.

- [x] T015 [US2] Write unit tests for `TaskService` in `backend/tests/unit/test_task_service.py`
- [ ] T016 [US2] Verify API deterministic responses and status codes (manual or script)
- [ ] T017 Verify strictly typed responses for all endpoints (Pydantic models)

## Dependencies & Execution Order

1. **Setup**: T001 -> T002 -> T003 -> T004
2. **Data**: T004 -> T005 -> T006
3. **Logic**: T006 -> T007
4. **API**: T007 -> [T008, T009, T010, T011, T012, T013] (Parallel) -> T014
5. **Validation**: T015, T016, T017

## Parallel Execution Opportunities

- After T007 (Service), all API endpoints (T008-T013) can be implemented in parallel.
- Tests (T015) can be written in parallel with API implementation.
