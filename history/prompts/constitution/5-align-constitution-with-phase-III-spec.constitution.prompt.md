---
id: 5
title: align-constitution-with-phase-III-spec
stage: constitution
date: 2026-02-06
surface: agent
model: claude-haiku-4-5-20251001
feature: todo-chatbot
branch: 003-frontend-application
user: unknown
command: /sp.constitution
labels: [constitution, ai-chatbot, phase-III, mcp, stateless]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - ".specify/memory/constitution.md"
tests:
 - none
---

## Prompt

# spec-4 — Phase III: Todo AI Chatbot

## Objective
Introduce an AI-powered conversational interface that allows users to manage todos using natural language, without affecting existing Todo functionality from Phase I & II.

The system must be stateless, tool-driven, auditable, and agent-controlled.

---

## Scope
Phase III adds:
- AI chatbot for todo management
- MCP-based task operations
- Stateless chat API
- Persistent conversation history
- Chat UI (no replacement of existing UI)

Out of scope:
- Voice input/output
- Streaming responses
- Multi-agent collaboration

---

## Success Criteria
Phase III is complete when:
- Users can add, list, update, complete, and delete tasks via chat
- AI uses MCP tools for all task operations
- Conversations resume after server restart
- Backend holds no in-memory chat state
- Existing Todo features continue to work

---

## Architecture Overview
ChatKit UI
→ FastAPI `/api/{user_id}/chat`
→ OpenAI Agents SDK
→ MCP Server (Official SDK)
→ Neon PostgreSQL

---

## Technology Stack
- Frontend: OpenAI ChatKit
- Backend: FastAPI (Python)
- AI: OpenAI Agents SDK
- MCP: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth

---

## Specification Breakdown
Phase III implementation is governed by the following specs:

- `spec-4.1-mcp-tools.md` — MCP server & tool contracts
- `spec-4.2-agent-behavior.md` — AI agent decision rules
- `spec-4.3-chat-api.md` — Stateless chat API & flow

All child specs are binding.

---

## Constraints
- No manual coding (Agentic Dev Stack only)
- AI agents cannot access DB directly
- MCP tools are the single mutation layer
- Backend must remain stateless

---

## Deliverables
- Working AI chatbot
- MCP server with task tools
- Persisted conversations
- Phase III specs
- Updated README

## Response snapshot

Updated the project constitution to align with detailed Phase III specifications, emphasizing MCP tools, stateless architecture, and additional constraints.

## Outcome

- ✅ Impact: Constitution aligned with detailed Phase III spec requirements including MCP constraints and stateless architecture
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: none
- 🧠 Reflection: Successfully incorporated specific constraints like "no direct DB access", "stateless backend", and "official MCP SDK"

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Not applicable