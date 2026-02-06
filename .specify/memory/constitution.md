<!--
Sync Impact Report:
Version change: 3.0.0 -> 3.0.1 (Phase III Specification Alignment)
Modified principles: Enhanced AI Agent Principles with MCP constraints
Added sections: MCP Tool Requirements, Stateless Architecture Constraints
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/spec-template.md ✅ validated (generic compliance)
- README.md ✅ updated
Follow-up TODOs: None
-->
# Todo Web App Constitution

## Core Principles

### I. Correctness & Quality (NON-NEGOTIABLE)
Correctness-first behavior in both backend and frontend; All API behavior must be deterministic and documented; All basic Todo features must function end-to-end.
<!-- Example: All API behavior must be deterministic and documented; Clear loading, error, and empty states in UI; Backend verifies identity independently of frontend -->

### II. Security & Isolation (NON-NEGOTIABLE)
Security-by-design with strict user isolation; No cross-user data access under any condition; Authentication must be stateless and token-based (JWT).
<!-- Example: Authorization must be enforced on every data operation; Users may only read or mutate their own tasks; Database queries must always filter by authenticated user ID; No implicit trust in URL parameters -->

### III. Spec-Driven Development (NON-NEGOTIABLE)
All code must be generated from specifications; Any change requires spec updates, not manual code edits; Traceable requirements from spec to code.
<!-- Example: All features must map directly to an explicit requirement; Spec-driven workflow enforced across all layers (frontend, backend, database) -->

### IV. Clear Separation of Concerns
Strict separation between Frontend (Next.js), Backend (FastAPI), Authentication (Better Auth), and Data (Neon Postgres); No leaky abstractions.
<!-- Example: Frontend must only consume authenticated APIs; Authentication logic must not rely on backend sessions; Environment secrets must not be hard-coded -->

### V. Production-Grade Architecture
System must be deployable, scalable, and suitable for real users; No mock or in-memory storage for final implementation.
<!-- Example: Responsive, mobile-first UI; Accessible components; Centralized API client; Persistent storage in Neon Serverless PostgreSQL -->

### VI. AI Agent Principles (NON-NEGOTIABLE)
AI-powered chatbot must be stateless, auditable, and tool-driven; All todo operations must be performed through explicit MCP tools only; No hallucinations or autonomous actions outside defined tools; AI agents cannot access DB directly.
<!-- Example: Chat interface must persist all conversations and messages; AI must confirm critical actions before execution; Agent must follow strict intent inference without making assumptions -->

## Project Scope

**Domain**: Multi-user, Full-Stack Todo Web Application with AI Chat Interface
**Tech Stack**: Next.js 16+ (App Router), Python FastAPI, SQLModel, Neon Serverless PostgreSQL, Better Auth, OpenAI Agents SDK, ChatKit, Official MCP SDK
**Boundaries**:
- RESTful API design following HTTP semantics
- Fixed technology stack (no substitutions)
- No in-memory storage (persistence required)
- Stateless authentication (JWT)
- Stateless backend (no in-memory chat state)
- AI agent uses only predefined MCP tools
- MCP tools are the single mutation layer
- Stateful conversations stored in database
- No voice input/output, streaming responses, or multi-agent collaboration

## Development Workflow

1. **Spec-First**: Update `/specs` definitions before touching code.
2. **Strict Isolation**: Ensure every feature works for multi-user scenarios immediately.
3. **Full-Stack Integration**: Frontend, Backend, Authentication, and Chat Interface must integrate correctly; no mocked layers in final PRs.
4. **Security Check**: Verify "User A cannot see User B's data" for every change.
5. **AI Compliance**: Verify all chatbot actions use MCP tools without hallucination; maintain audit trail of all operations.
6. **MCP Compliance**: Verify AI agents only use MCP tools for database operations; no direct DB access allowed.
7. **Stateless Verification**: Verify backend holds no in-memory chat state; conversations resume after server restart.

## Governance

All code changes must comply with this constitution. Amendments require documentation and approval. Phase III constraints (AI Chat Interface, MCP Tools, Conversation Persistence, Stateless Backend) strictly supersede previous rules when conflicting. All chatbot interactions must be stateless on the backend but maintain DB-backed history. No manual coding allowed - Agentic Dev Stack workflow only.

**Version**: 3.0.1 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-02-06