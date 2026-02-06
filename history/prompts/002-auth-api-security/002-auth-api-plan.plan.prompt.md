---
id: 002
title: auth-api-plan
stage: plan
date: 2026-01-09
surface: agent
model: claude-opus-4-5-20251101
feature: auth-api-security
branch: 002-auth-api-security
user: user
command: /sp.plan
labels: ["plan", "auth", "security", "jwt", "fastapi"]
links:
  spec: specs/002-auth-api-security/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-auth-api-security/plan.md
 - specs/002-auth-api-security/research.md
 - specs/002-auth-api-security/data-model.md
 - specs/002-auth-api-security/quickstart.md
tests:
 - none
---

## Prompt

Todo Full-Stack Web Application – Spec 2: Authentication & API Security

Implementation strategy:
1. Configure Better Auth on the Next.js frontend:
   - Enable JWT plugin
   - Set shared secret via environment variable (BETTER_AUTH_SECRET)
   - Ensure token expiry is configured (e.g., 7 days)

2. Implement FastAPI JWT middleware:
   - Extract token from Authorization header
   - Verify signature using shared secret
   - Decode JWT to get user ID and email
   - Handle invalid, expired, or missing tokens with HTTP 401

3. Update backend endpoints to enforce ownership:
   - Filter all task queries by authenticated user ID from JWT
   - Reject operations if user ID from JWT does not match task owner
   - Ensure all CRUD endpoints and PATCH completion endpoint are secured

4. Validate stateless authentication:
   - Backend does not rely on frontend session
   - All authorization decisions made locally using JWT claims

5. Prepare backend for frontend integration in Spec 3:
   - Ensure API responses include proper status codes and error messages
   - Confirm modular middleware is reusable and maintainable

Validation & review:
- Test JWT issuance from frontend and verify token decoding in backend
- Confirm unauthorized requests return HTTP 401
- Test multi-user task isolation to prevent cross-user data access
- Review middleware performance and correctness

Delivery:
- Backend fully secured with JWT authentication
- Task ownership enforced across all endpoints
- Ready for frontend integration in Spec 3

## Response snapshot

Created implementation plan for Authentication & API Security.
- Validated constitution compliance (No violations).
- Researched Better Auth JWT integration with FastAPI (PyJWT selection).
- Designed data model enforcing strict user isolation.
- Created quickstart guide for development setup.
- Updated Secure Auth Specialist agent context.

## Outcome

- ✅ Impact: Established clear roadmap for secure, stateless JWT authentication.
- 🧪 Tests: N/A
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: Research confirmed PyJWT is the standard choice. Strict isolation requirement correctly propagated to data model.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
