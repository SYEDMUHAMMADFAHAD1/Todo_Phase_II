# Phase 0 Research: Authentication & API Security

**Date**: 2026-01-10 | **Branch**: `002-auth-api-security` | **Status**: Complete

## Executive Summary

All research questions have been resolved through examination of existing codebase, specification review, and best practices analysis. The project is ready for Phase 1 design with clear architectural decisions confirmed.

---

## Decision 1: JWT Verification Strategy

**Decision**: Use PyJWT library with HMAC-SHA256 for stateless token verification.

**Rationale**:
- Already implemented in `backend/auth.py` with production-grade error handling
- HMAC-SHA256 is industry standard for JWT signing with shared secrets
- Stateless verification aligns with Constitution requirement for "no session storage"
- Better Auth (frontend/auth layer) will issue tokens; backend only verifies signatures

**Alternatives Considered**:
1. ~~RSA Public Key Verification~~ - Requires public key infrastructure; HMAC simpler for monolithic backend
2. ~~Session-based Authentication~~ - Violates Constitution; requires server-side state
3. ~~OAuth2 with introspection endpoint~~ - Over-engineered for internal microservice; JWT sufficient

**Implementation Notes**:
- Secret sourced from `BETTER_AUTH_SECRET` environment variable
- Token expiration validated at verification time (PyJWT handles automatically)
- "sub" claim maps to user ID (standard JWT convention)

---

## Decision 2: Middleware Integration Pattern

**Decision**: Use FastAPI dependency injection (`Depends(get_current_user)`) on each endpoint rather than global middleware.

**Rationale**:
- Allows selective protection (health check remains unprotected)
- Per-endpoint granularity enables future public endpoints
- FastAPI native pattern; better error handling and documentation
- Simpler to test individual endpoints with mock user contexts

**Alternatives Considered**:
1. ~~Global middleware~~ - Would require router exclusion patterns; less flexible
2. ~~Manual header inspection~~ - Code duplication across endpoints

---

## Decision 3: User Identity Source

**Decision**: Extract user identity exclusively from JWT "sub" claim (subject).

**Rationale**:
- JWT claims are cryptographically signed; client cannot forge them
- URL parameters are untrusted; relying on them enables privilege escalation
- Spec requirements FR-003 and FR-005 mandate this approach

---

## Decision 4: Database Query Filtering

**Decision**: Filter all queries at service layer by authenticated user_id.

**Rationale**:
- Prevents data leakage from application logic bugs
- Defense in depth principle
- Spec requirement FR-004: "Filter all database queries by authenticated user_id"

---

## Decision 5: Error Response Strategy

**Decision**: 401 Unauthorized for auth failures; 404 Not Found for non-existent resources.

**Rationale**:
- 401 is HTTP standard for authentication failures
- 404 prevents information leakage (user shouldn't know if task belongs to someone else)
- Aligns with Spec edge case preferences

---

## Summary of Key Unknowns Resolved

| Unknown | Resolution |
|---------|-----------|
| JWT algorithm | HMAC-SHA256 (Better Auth standard) |
| Integration pattern | Dependency injection per-endpoint |
| User ID source | JWT "sub" claim only |
| Query filtering | Service layer (indexed queries) |
| Error codes | 401 for auth, 404 for not found |
| Secret rotation | Environment-based reload |
| Testing approach | Three-layer (unit, integration, E2E) |

---

## Next Steps: Phase 1 Design

Phase 1 will formalize:
1. Data model with user_id relationships
2. API contracts with auth headers
3. Implementation quickstart guide
