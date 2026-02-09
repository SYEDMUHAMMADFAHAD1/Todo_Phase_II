---
id: 1
title: "constitution-update-mcp-server-integration"
stage: "constitution"
date: "2026-02-07"
surface: "agent"
model: "default"
feature: "mcp-server-ai-task-tools"
branch: "main"
user: "default"
command: "/sp.constitution"
labels: ["constitution", "mcp", "ai-tools", "todo-app"]
links:
  spec: "specs/005-mcp-server-ai-task-tools/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
  - ".specify/templates/plan-template.md"
  - ".specify/templates/spec-template.md"
  - ".specify/templates/tasks-template.md"
tests: []
outcome: "Successfully updated the project constitution to reflect the new MCP Server & AI Task Tools Integration principles. The constitution now emphasizes tool-driven AI behavior, MCP as the single execution layer, stateless tools with database-backed state, clear separation between reasoning and execution, and deterministic operations."
evaluation: "The constitution update was successful. All required principles from the specification have been incorporated, and dependent templates have been checked for alignment. The new constitution supports the MCP server integration requirements while maintaining the project's core values."
---

# Constitution Update: MCP Server & AI Task Tools Integration

## Prompt Text

Project: Todo Full-Stack Web Application — Phase III (Spec 5)

Spec Name: MCP Server & AI Task Tools Integration

Core Principles:
- Tool-driven AI behavior (no direct DB access by agent)
- MCP as the single execution layer for task actions
- Stateless MCP tools with database-backed state
- Clear separation between reasoning (Agent) and execution (Tools)
- Deterministic, auditable task operations

Key Standards:
- AI agents must never mutate data directly
- All task operations must go through MCP tools
- MCP tools must be stateless and idempotent where possible
- Each tool invocation must be traceable and logged
- Tool outputs must be structured and predictable

Architecture Rules:
- Agent reasons → calls MCP tools → receives results
- MCP server exposes task operations as tools
- MCP tools interact with database only
- FastAPI orchestrates agent execution
- No business logic inside prompts

Security Rules:
- user_id must be passed explicitly to every tool
- Task ownership enforced at tool level
- Unauthorized access must fail safely
- JWT validation handled before agent execution

Constraints:
- MCP Server: Official MCP SDK only
- Backend: Python FastAPI
- AI Framework: OpenAI Agents SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT)
- No frontend changes in this spec

Out of Scope:
- Chat UI enhancements
- Prompt tuning or personality design
- Advanced agent memory strategies
- Analytics or monitoring

Success Criteria:
- MCP server exposes all task tools
- AI agent uses MCP tools correctly
- Tasks can be created, listed, updated, completed, and deleted via chat
- No direct DB access from agent
- System remains stateless and restart-safe

## Response Text

Updated the project constitution to reflect the new MCP Server & AI Task Tools Integration principles. The constitution now emphasizes tool-driven AI behavior, MCP as the single execution layer, stateless tools with database-backed state, clear separation between reasoning and execution, and deterministic operations. The document includes all required constraints and security rules from the specification.