---
id: 6
title: "amend-constitution-chatbot-ui-stateless-api"
stage: "constitution"
date_iso: "2026-02-07"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "chatbot-ui-stateless-api"
branch: "003-frontend-application"
user: "user"
command: "/sp.constitution Project: Todo Full-Stack Web Application — Phase III (Spec 4)"
labels: ["constitution", "phase-iii", "chatbot", "stateless-architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - .specify/memory/constitution.md
tests_yaml: |
  - none
---

# Constitution Update: Chatbot UI & Stateless Chat API Foundation

## Overview
Updated the project constitution to align with Phase III requirements for Chatbot UI & Stateless Chat API Foundation.

## Changes Made
- Added "Stateless Architecture" principle (VI) emphasizing no in-memory session state
- Added "Database-Driven Conversation State" principle (VII) focusing on DB as single source of truth
- Updated project scope to include chatbot UI and stateless API requirements
- Modified development workflow to include stateless verification and API determinism
- Updated governance to emphasize Phase III constraints

## Original Prompt
```
/sp.constitution

Project: Todo Full-Stack Web Application — Phase III (Spec 4)

Spec Name: Chatbot UI & Stateless Chat API Foundation

Core Principles:
- Stateless backend architecture (no in-memory session state)
- Clear separation of concerns (UI, API, Agent, MCP handled independently)
- Deterministic request → response behavior
- Database as the single source of truth for chat history
- Spec-driven development (spec → plan → tasks → implementation)

Key Standards:
- Every chat request must be fully reproducible from database state
- No backend state stored between requests
- Conversation context must be reconstructed from persisted messages
- API responses must be predictable and structured
- Frontend must reflect backend state accurately

Architecture Rules:
- Frontend communicates only via HTTP API
- Backend does not depend on frontend runtime state
- Conversation continuity relies solely on database records
- Authentication context must be enforced per request

Constraints:
- Frontend: OpenAI ChatKit only
- Backend: Python FastAPI only
- AI Logic: OpenAI Agents SDK (no custom LLM wrappers)
- Database: Neon Serverless PostgreSQL
- ORM: SQLModel
- Authentication: Better Auth (JWT-based)
- No MCP tool execution in this spec

Out of Scope:
- MCP server implementation
- Task-manipulation tools
- Advanced agent reasoning
- Prompt optimization
- UI animations or visual polish beyond functional chat

Success Criteria:
- Chat UI renders and sends messages successfully
- Stateless POST /api/{user_id}/chat endpoint works
- Conversations and messages persist in database
- Conversation resumes correctly after server restart
- No backend memory/state dependency exists
```

## Response Summary
Updated the constitution file (.specify/memory/constitution.md) to version 3.1.0, incorporating new principles around stateless architecture and database-driven conversation state. The update emphasizes that the backend must maintain no in-memory session state, every chat request must be reproducible from database state, and conversations must rely solely on database records for continuity.

## Outcome
The constitution now properly reflects the requirements for the Chatbot UI & Stateless Chat API Foundation phase, ensuring all future development adheres to stateless architecture principles and database-driven conversation management.
