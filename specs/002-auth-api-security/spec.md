# Feature Specification: Authentication & API Security

**Feature Branch**: `002-auth-api-security`
**Created**: 2026-01-09
**Status**: Draft
**Input**: User description based on "Todo Full-Stack Web Application – Spec 2: Authentication & API Security"
**Constitution Compliance**: All implementations must adhere to the project constitution principles

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
-->

### User Story 1 - Secure API Access (Priority: P1)

As a spec-driven developer, I need the backend to block unauthenticated requests so that task data remains private.

**Why this priority**: Fundamental security requirement; without this, user isolation is impossible.

**Independent Test**: Can be fully tested using standard HTTP clients by sending requests with valid, invalid, and missing tokens.

**Acceptance Scenarios**:

1. **Given** a request to `/tasks` without an `Authorization` header, **When** the request is sent, **Then** the server returns 401 Unauthorized.
2. **Given** a request with an invalid/expired JWT, **When** the request is sent, **Then** the server returns 401 Unauthorized.
3. **Given** a request with a valid Better Auth JWT, **When** the request is sent, **Then** the server processes the request and returns 200 OK.

---

### User Story 2 - User Isolation (Priority: P1)

As a user, I want to see only my own tasks so that my todo list is not cluttered or exposed to others.

**Why this priority**: Core functional requirement for a multi-user application.

**Independent Test**: Create two users (A and B), perform operations as User A, and verify User B cannot see or modify User A's data.

**Acceptance Scenarios**:

1. **Given** User A has 3 tasks and User B has 0 tasks, **When** User B requests `GET /tasks`, **Then** the response is an empty list.
2. **Given** User A has a task with ID 123, **When** User B sends `DELETE /tasks/123`, **Then** the server returns 404 Not Found (or 403 Forbidden, but 404 preferred for security).
3. **Given** User A creates a task, **When** the task is saved to the DB, **Then** the `user_id` field matches User A's ID from the JWT token, ignoring any ID in the request body.

---

### Edge Cases

- What happens when the Better Auth secret is rotated? (Tokens signed with old secret should fail).
- How does system handle malformed JWT headers (e.g., missing "Bearer " prefix)? (Return 401).
- What happens if a user is deleted but their token is still valid? (Token validation succeeds, but DB lookup might fail if referenced - strictly token verification should pass, but operation might fail if user checks required).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST verify the JWT signature of every incoming request to protected endpoints using the Better Auth shared secret.
- **FR-002**: System MUST reject requests with missing, expired, or invalid tokens with HTTP 401.
- **FR-003**: System MUST extract `user_id` from the valid JWT payload and make it available to request handlers.
- **FR-004**: System MUST filter all database queries by the authenticated `user_id`.
- **FR-005**: System MUST automatically assign the authenticated `user_id` to new tasks upon creation, overriding any client-provided value.
- **FR-006**: System MUST not rely on session cookies or server-side session storage; strictly stateless JWT verification.

### Key Entities

- **User Identity**: Extracted strictly from JWT `sub` or id claim. Not a new database table in this spec (assuming Better Auth manages user tables/data externally or in separate schema, focus here is verification).
- **Task**: Existing entity owner field must correspond to the JWT subject.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of requests without valid tokens are rejected by the backend middleware.
- **SC-002**: Users can strictly perform CRUD operations on their own data (0% cross-user data leakage).
- **SC-003**: API response time overhead for token verification is less than 50ms.
- **SC-004**: Verification logic strictly adheres to Better Auth JWT standard (HMAC/RSA specific to config).

