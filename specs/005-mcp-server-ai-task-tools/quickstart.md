# Quickstart Guide: MCP Server & AI Task Tools

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed
- PostgreSQL (or Neon Serverless PostgreSQL connection)
- Better Auth configured for user authentication
- OpenAI API key
- Official MCP SDK
- SQLModel for database operations

## Environment Setup

### Backend Configuration
1. Create `.env` file in the backend directory:
```bash
DATABASE_URL="postgresql://user:password@host:port/database"
OPENAI_API_KEY="your-openai-api-key"
BETTER_AUTH_SECRET="your-auth-secret"
BETTER_AUTH_URL="http://localhost:3000"
```

### Frontend Configuration
1. Create `.env.local` file in the frontend directory:
```bash
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
NEXT_PUBLIC_OPENAI_API_KEY="your-openai-api-key"
```

## Running the Application

### Backend Setup
1. Navigate to backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Install MCP SDK: `pip install mcp`
4. Run database migrations: `python -m src.core.db init`
5. Start the server: `uvicorn src.main:app --reload --port 8000`

### Frontend Setup
1. Navigate to frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Visit `http://localhost:3000` in your browser

## MCP Server Configuration

### Initializing the MCP Server
The MCP server is initialized as part of the FastAPI application lifecycle. The tools are registered automatically when the application starts.

### Available MCP Tools

1. **add_task**
   - Creates a new task for the authenticated user
   - Parameters: `title` (required), `description` (optional)
   - Returns: Task ID and success status

2. **list_tasks**
   - Lists tasks for the authenticated user
   - Parameters: `filter` (optional: 'all', 'pending', 'completed')
   - Returns: Array of task objects

3. **update_task**
   - Updates an existing task
   - Parameters: `task_id` (required), `title` (optional), `description` (optional)
   - Returns: Updated task object

4. **complete_task**
   - Marks a task as completed
   - Parameters: `task_id` (required)
   - Returns: Updated task object

5. **delete_task**
   - Deletes a task
   - Parameters: `task_id` (required)
   - Returns: Success status

## Agent Integration

The AI agent is configured to use the MCP tools for all task-related operations. When a user sends a request related to tasks, the agent will:

1. Parse the user's intent
2. Select the appropriate MCP tool
3. Call the tool with the required parameters
4. Receive the result and formulate a response

## Key Features

1. **Stateless Architecture**: No session state stored between requests
2. **Database-Driven Operations**: All task operations go through the database via MCP tools
3. **Secure Authentication**: JWT-based authentication with user isolation
4. **Persistent Storage**: All tasks stored in database
5. **AI-Powered Interface**: Natural language interaction with tasks

## Development Workflow

1. Run database migrations to create required tables
2. Implement MCP tools following the defined schemas
3. Register tools with the MCP server
4. Connect tools to the existing task service layer
5. Test agent interaction with MCP tools
6. Verify stateless behavior by restarting backend during operations