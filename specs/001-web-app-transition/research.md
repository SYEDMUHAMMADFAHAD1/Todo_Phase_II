# Phase 0: Research Findings

## 1. Authentication Strategy: Better Auth & FastAPI

**Decision**: Use `better-auth` (TypeScript library) on the frontend for auth UI and session management, and JWT verification on the backend.

**Rationale**:
- `better-auth` provides a complete, secure auth flow (Signup, Signin, Session) for Next.js.
- FastAPI only needs to verify the JWT signature, keeping the backend stateless.

**Implementation Details**:
- **Shared Secret**: Both `better-auth` (Frontend) and FastAPI (Backend) must share a `BETTER_AUTH_SECRET`.
- **Flow**:
  1. Frontend (Better Auth) -> Login -> Returns Session/JWT.
  2. Frontend -> Request API -> Include `Authorization: Bearer <token>`.
  3. Backend -> Middleware -> Verify Signature -> Extract User ID.

## 2. Project Structure

**Decision**: Monorepo with strict `frontend/` and `backend/` separation ("Option 2").

**Rationale**:
- Next.js and Python ecosystems have different tooling (npm vs pip/uv).
- Prevents dependency conflicts.
- Allows independent scaling and deployment.

**Structure**:
- `/frontend` (Next.js 16 + Tailwind + Better Auth)
- `/backend` (FastAPI + SQLModel + Alembic)

## 3. Frontend Testing Stack

**Decision**: Vitest + React Testing Library for Unit/Component; Playwright for E2E.

**Rationale**:
- **Vitest**: Native ESM support (essential for Next.js), fast execution, Jest-compatible API.
- **Playwright**: Official Next.js recommendation, better handling of async components/hydration than Cypress.

## 4. Database: SQLModel + Neon Postgres

**Decision**: SQLModel with `asyncpg` driver.

**Rationale**:
- **Async**: `asyncpg` is the most performant async driver for Postgres in Python.
- **SQLModel**: Combines Pydantic verification with SQLAlchemy ORM, ideal for FastAPI.
- **Connection**: `postgresql+asyncpg://user:pass@host/db?ssl=require`

## 5. Backend Architecture (Spec 1 Refinement)

**Decision**: Modular Application Structure

**Rationale**: Explicitly requested in Spec 1 plan. Allows scaling and clear separation of concerns.

**Structure**:
```text
backend/src/
  api/
    routers/ (endpoints)
  services/ (business logic, CRUD)
  models/ (SQLModel entities)
  core/ (config, db, security)
```

**Decision**: Pre-Auth Identity Handling (Spec 1 only)

**Rationale**: Spec 1 requires validation of Task CRUD before Auth is integrated.

**Implementation**: define `owner_id` field. API endpoints accept `user_id` as path parameter (TEMPORARY).

**Risk**: Insecure. Must be replaced in Spec 2 (Auth) with JWT extraction.
