ID: "001-research-better-auth-nextjs-fastapi"
TITLE: "Research Better Auth NextJS FastAPI"
STAGE: "misc"
DATE_ISO: "2026-01-09"
SURFACE: "agent"
MODEL: "claude-opus-4-5-20251101"
FEATURE: "001-web-app-transition"
BRANCH: "001-web-app-transition"
USER: "User"
COMMAND: "research"
LABELS: ["research", "better-auth", "nextjs", "fastapi", "sqlmodel", "neon"]
LINKS:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
FILES_YAML:
  - "history/prompts/001-web-app-transition/001-research-better-auth-nextjs-fastapi.misc.prompt.md"
TESTS_YAML:
PROMPT_TEXT: |
  Please research the following for the Todo Full-Stack Web Application:
  1. Confirm what "Better Auth" refers to in the context of Next.js and FastAPI. Is it a specific library (like `better-auth`)? Look for "better-auth" documentation or patterns for "Next.js FastAPI JWT auth".
  2. Identify best practices for structuring a Next.js 16 App Router + FastAPI project. Should they be in `backend/` and `frontend/` directories? (References "Option 2" in plan template).
  3. Determine the recommended testing stack for Next.js 16 App Router (Vitest vs Jest vs Playwright).
  4. Verify SQLModel + Neon Serverless PostgreSQL connection strings and async patterns.

  Output findings in a format suitable for inclusion in `research.md`.
RESPONSE_TEXT: |
  Conducted research on Better Auth, project structure, testing stack, and SQLModel/Neon integration.

  Findings:
  1. **Better Auth**: Identified as `better-auth` library for Next.js. Integration with FastAPI requires shared secret JWT verification.
  2. **Structure**: Confirmed `frontend/` and `backend/` directory separation as best practice.
  3. **Testing**: Recommended Vitest for unit/integration and Playwright for E2E for Next.js 16.
  4. **Database**: Verified `postgresql+asyncpg` scheme for SQLModel with Neon.
OUTCOME: "Research completed successfully."
EVALUATION: "Gathered necessary technical details for the implementation plan."
