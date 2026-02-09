<!-- Sync Impact Report:
  - Version change: N/A → 1.0.0
  - Modified principles: N/A (new constitution)
  - Added sections: Core Principles (6), Additional Constraints, Development Workflow
  - Removed sections: N/A
  - Templates requiring updates: 
    - .specify/templates/plan-template.md ✅ updated
    - .specify/templates/spec-template.md ✅ updated  
    - .specify/templates/tasks-template.md ✅ updated
    - .specify/templates/commands/*.md ✅ reviewed
  - Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Tool-Driven AI Behavior
AI agents must never access the database directly. All data operations must be performed through MCP tools. This ensures centralized control, auditability, and consistent business logic enforcement. Agents are responsible for reasoning and decision-making, while tools handle execution.

### II. MCP as Single Execution Layer
The MCP server serves as the single source of truth for all task operations. All task-related actions (create, read, update, delete) must flow through MCP tools. This creates a clean separation between AI reasoning and system execution, enabling better monitoring, logging, and security controls.

### III. Stateless MCP Tools with Database-Backed State
MCP tools must remain stateless, with all state persisted in the database. This ensures system reliability, scalability, and resilience to server restarts. Each tool invocation must be self-contained and not rely on in-memory state from previous invocations.

### IV. Clear Separation Between Reasoning and Execution
There must be a strict separation between AI reasoning (handled by the agent) and execution (handled by MCP tools). The AI agent determines what actions to take based on user input and context, while MCP tools execute those actions reliably and securely.

### V. Deterministic and Auditable Operations
All task operations must be deterministic and fully auditable. Each operation must be logged with sufficient context to reproduce or verify the action. This enables debugging, compliance, and system reliability.

### VI. Spec-Driven Development (NON-NEGOTIABLE)
All features must begin with a well-defined specification before implementation. Specifications must include user stories, acceptance criteria, and test scenarios. Implementation must strictly follow the specification, with changes to the spec required for any deviations.

## Additional Constraints

### Technology Stack Requirements
- MCP Server: Official MCP SDK only
- Backend: Python FastAPI
- AI Framework: OpenAI Agents SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT)

### Security Requirements
- user_id must be passed explicitly to every tool
- Task ownership enforced at tool level
- Unauthorized access must fail safely
- JWT validation handled before agent execution

### Performance Standards
- Tool response times under 2 seconds for 95% of requests
- System must handle 1000 concurrent users
- Database queries must be optimized with proper indexing

## Development Workflow

### Code Review Requirements
- All pull requests must include specification reference
- MCP tool changes require security review
- AI integration changes require test coverage verification
- Database schema changes require migration plan

### Testing Gates
- Unit tests for all MCP tools (90%+ coverage)
- Integration tests for AI-MCP interactions
- End-to-end tests for complete user workflows
- Security tests for authentication and authorization

### Deployment Approval Process
- Automated tests must pass
- Performance benchmarks met
- Security scan clear
- Manual QA sign-off for user-facing changes

## Governance

The constitution supersedes all other development practices. Amendments require formal documentation, team approval, and migration planning. All pull requests and reviews must verify compliance with constitutional principles. Complexity must be justified with clear benefits. Use this constitution for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07