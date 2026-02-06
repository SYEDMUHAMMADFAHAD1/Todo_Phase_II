# Implementation Plan: Web App Transition (Phase II - Spec 1 Focus)

**Branch**: `001-web-app-transition` | **Date**: 2026-01-09 | **Spec**: [specs/001-web-app-transition/spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-web-app-transition/spec.md`

## Summary

This plan breaks down the "Web App Transition" into three specifications. **Spec 1** focuses on establishing the Backend Core and Data Layer using FastAPI and Neon PostgreSQL, setting the foundation for authentication and frontend integration in subsequent specs.

## Technical Context

**Language/Version**: Python 3.12 (Backend), TypeScript 5.x (Frontend - Future)
**Primary Dependencies**: FastAPI, SQLModel, asyncpg, alembic
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest
**Target Platform**: Web
**Project Type**: Full-Stack Web Application (Monorepo)
**Performance Goals**: < 200ms API p95
**Constraints**: Modular Architecture, Strict Isolation (Prepared), Persistent Storage
**Scale/Scope**: Spec 1 covers pure backend logic.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Spec-Driven Development Compliance**: All implementation must be based on specifications. **COMPLIANT**
2. **Correctness & Security**: Spec 1 prepares for security (owner_id field) but temporarily exposes user_id in path for testing. **WARNING: Temporary Insecurity for Spec 1 Validation only.**
3. **Separation of Concerns**: Backend structure strictly separated (api/services/models). **COMPLIANT**
4. **Production-Grade**: Real DB (Neon) used from day one. **COMPLIANT**
5. **Test-First Approach**: TDD mandatory. **COMPLIANT**

## Project Structure

### Documentation (this feature)

```text
specs/001-web-app-transition/
├── plan.md              # This file
├── research.md          # Research findings
├── data-model.md        # Entity definitions
├── quickstart.md        # Developer setup
├── contracts/           # API Definitions
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
backend/src/
├── api/
│   ├── routers/      # API Endpoints
│   └── dependencies.py
├── core/
│   ├── config.py     # Settings
│   └── db.py         # Database connection
├── models/           # SQLModel Entities
├── services/         # Business Logic
└── main.py           # Entrypoint

tests/
├── conftest.py
└── unit/
```

**Structure Decision**: Modular "Service-Repository" pattern within FastAPI to ensures scalability.

## Implementation Phases (Spec 1)

### 1. Project Initialization
- Initialize FastAPI project with modular structure.
- Configure `core/config.py` and `core/db.py` (SQLModel + Async Engine).

### 2. Data Layer
- Define `Task` model in `models/task.py` with fields: `id`, `title`, `description`, `completed`, `created_at`, `updated_at`, `owner_id`.
- Create Alembic migration scripts.

### 3. API Implementation
- Implement `services/task_service.py` for CRUD operations.
- Implement `api/routers/tasks.py` with endpoints:
  - `GET /api/{user_id}/tasks`
  - `POST /api/{user_id}/tasks`
  - `GET /api/{user_id}/tasks/{id}`
  - `PUT /api/{user_id}/tasks/{id}`
  - `DELETE /api/{user_id}/tasks/{id}`
  - `PATCH /api/{user_id}/tasks/{id}/complete`

### 4. Validation
- Run tests to verify persistence and API behavior.
- Ensure deterministic HTTP status codes (200, 201, 204, 404).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Insecure API (Spec 1) | Needed for backend validation before Auth | Mocking auth would hide DB issues |
