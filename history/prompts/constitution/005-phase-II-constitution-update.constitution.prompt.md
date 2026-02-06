---
id: 5
title: phase-II-constitution-update
stage: constitution
date: 2026-01-09
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: main
user: user
command: sp.constitution
labels: ["constitution", "phase-II", "refactoring"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/tasks-template.md
 - README.md
tests:
 - none
---

## Prompt

Project: Todo Full-Stack Web Application (Spec-Driven, Multi-User, Secure)

Core principles:
- Correctness-first backend and frontend behavior
- Security-by-design with strict user isolation
- Spec-driven development with traceable requirements
- Clear separation of concerns (frontend, backend, auth, data)
- Production-grade architecture suitable for real users

Key standards:
- All features must map directly to an explicit requirement
- All API behavior must be deterministic and documented
- Authentication must be stateless and token-based (JWT)
- Authorization must be enforced on every data operation
- Frontend must only consume authenticated APIs
- No cross-user data access under any condition

Architecture standards:
- Frontend: Next.js 16+ using App Router and modern component patterns
- Backend: FastAPI with modular routing and dependency injection
- ORM: SQLModel with explicit schema definitions
- Database: Neon Serverless PostgreSQL with persistent storage
- Authentication: Better Auth (frontend) + JWT verification (backend)
- Spec-driven workflow enforced across all layers

Security standards:
- All API endpoints require valid JWT after authentication is enabled
- JWT signature verification must use a shared secret
- Token expiration must be enforced
- User identity must be derived from JWT, not client input
- Task ownership must be verified on every CRUD operation
- Unauthorized requests must return HTTP 401

Data integrity standards:
- Each task must be owned by exactly one user
- Users may only read or mutate their own tasks
- Database queries must always filter by authenticated user ID
- No implicit trust in URL parameters for user identity

Frontend standards:
- Responsive, mobile-first UI
- Accessible components and readable layouts
- Centralized API client with automatic JWT attachment
- Clear loading, error, and empty states
- Protected routes for authenticated-only views

Constraints:
- Technology stack is fixed and must not be substituted
- RESTful API design must follow HTTP semantics
- No mock or in-memory storage for final implementation
- Authentication logic must not rely on backend sessions
- Environment secrets must not be hard-coded
- Code must be readable, modular, and maintainable

Success criteria:
- All basic Todo features function end-to-end
- Multiple users can operate simultaneously with full isolation
- Unauthorized access is fully blocked
- Backend verifies identity independently of frontend
- Frontend, backend, and database integrate correctly
- System is deployable and production-ready

## Response snapshot

Updated the Constitution to Version 2.0.0, transitioning the project from a Phase I In-Memory Console Application to a Phase II Full-Stack Web Application to support the new requirements.

Key updates:
1. Core Principles: Revised to emphasize Correctness, Security & Isolation, Separation of Concerns, and Production-Grade Architecture.
2. Tech Stack: Explicitly defined Next.js, FastAPI, Neon Postgres, and Better Auth.
3. Templates: Updated plan-template.md and tasks-template.md to align with new principles (security, persistence).
4. README: Updated to reflect the Phase II evolution and new stack.

## Outcome

- ✅ Impact: Successfully transitioned project governance to Phase II standards.
- 🧪 Tests: Validated template consistency manually.
- 📁 Files: Updated constitution.md, plan-template.md, tasks-template.md, README.md.
- 🔁 Next prompts: /sp.plan to begin planning new features under new constitution.
- 🧠 Reflection: The transition required careful rewriting of all principles to move from a restrictive in-memory model to a secure, layered full-stack model.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
