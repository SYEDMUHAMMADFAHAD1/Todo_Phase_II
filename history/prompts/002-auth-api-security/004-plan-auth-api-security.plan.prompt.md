---
id: 004
title: Plan auth API security
stage: plan
date: 2026-01-10
surface: agent
model: claude-opus-4-5
feature: 002-auth-api-security
branch: 002-auth-api-security
user: user
command: /sp.plan
labels: [authentication, security, jwt, fastapi, spec-driven]
links:
  spec: /specs/002-auth-api-security/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-auth-api-security/plan.md
  - specs/002-auth-api-security/research.md
  - specs/002-auth-api-security/data-model.md
  - specs/002-auth-api-security/quickstart.md
  - specs/002-auth-api-security/contracts/openapi.yaml
  - specs/002-auth-api-security/contracts/auth-contract.md
tests:
  - None (Phase 2 generation of tasks.md will create test specifications)
---

## Prompt

```
Todo Full-Stack Web Application – Spec 2: Authentication & API Security

Steps:
1. Enable JWT issuance in Better Auth
   - Configure JWT plugin
   - Set BETTER_AUTH_SECRET via environment variables

2. Add JWT verification middleware in FastAPI
   - Extract token from Authorization header
   - Verify signature and expiration
   - Decode user identity from JWT claims

3. Secure all API routes
   - Require valid JWT for every endpoint
   - Return HTTP 401 for missing or invalid tokens

4. Enforce task ownership
   - Filter all queries by authenticated user ID
   - Prevent cross-user read/write operations

5. Validate security behavior
   - Test valid, invalid, and expired tokens
   - Verify multi-user isolation

Outcome:
- Stateless, secure API
- User isolation guaranteed
- Backend ready for frontend integration
```

## Response snapshot

### Phase 0: Research Complete
- JWT verification with HMAC-SHA256 (already implemented in backend/auth.py)
- FastAPI dependency injection for per-endpoint authentication
- User identity extracted from JWT "sub" claim (JWT-only source of truth)
- Database query filtering at service layer (defense in depth)
- 401 for auth failures, 404 for non-existent resources (security by obscurity)
- Environment-based secret rotation with container restart
- Three-layer test suite (unit, integration, E2E)

### Phase 1: Design & Contracts Complete
Generated artifacts:
- `research.md` - 8 architectural decisions with rationale
- `data-model.md` - Entity relationships, validation, isolation guarantees
- `contracts/openapi.yaml` - OpenAPI 3.0 specification for 6 endpoints
- `contracts/auth-contract.md` - Authentication flow, error handling, test patterns
- `quickstart.md` - Implementation roadmap with code examples

### Data Model
- **UserIdentity**: In-memory (JWT claims) - stateless, extracted per request
- **Task**: PostgreSQL with user_id indexed and filtered on all queries

### API Contracts
- All endpoints require `Authorization: Bearer <JWT>` header
- 401 for auth failures; 404 for not-found OR not-owned tasks
- 6 task endpoints secured: POST, GET (list/single), PUT, DELETE, PATCH

### Constitution Validation
✅ All 5 principles satisfied:
1. Spec-driven: Implementation derived from spec.md (FR-001 through FR-006)
2. Security: Mandatory JWT verification + user isolation at DB layer
3. Separation of concerns: Frontend/Backend/Auth/Data clearly demarcated
4. Production-grade: Persistent storage, proper error handling, async patterns
5. Test-first: Three-layer test coverage planned (unit, integration, E2E)

## Outcome

- ✅ Impact: Complete architectural foundation for auth & security. Backend JWT verification already implemented; Phase 1 provides integration roadmap and contracts for implementation phase.
- 🧪 Tests: Test specifications will be generated in Phase 2 (tasks.md). Test structure: unit (JWT validation), integration (multi-user isolation), E2E (full workflows).
- 📁 Files: 6 new artifacts created (research.md, data-model.md, 2 contract files, quickstart.md, updated plan.md).
- 🔁 Next prompts: `/sp.tasks` command to generate tasks.md with granular implementation tasks for each endpoint and test case specifications.
- 🧠 Reflection: Planning workflow successfully translated user requirements into structured architectural decisions. All unknowns resolved through research phase. No Constitution violations. Ready for implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - smooth execution through all phases
- Graders run and results: Constitution check passed all 5 principles; no violations detected
- Prompt variant: Standard planning workflow (research → design → contracts)
- Next experiment: Execute `/sp.tasks` to generate implementation tasks
