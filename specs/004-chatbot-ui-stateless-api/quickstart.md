# Quickstart Guide: Chatbot UI & Stateless Chat API

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- PostgreSQL (or Neon Serverless PostgreSQL connection)
- Better Auth configured for user authentication
- OpenAI API key
- OpenAI Agents SDK configured

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
3. Run database migrations: `python -m src.core.db init`
4. Start the server: `uvicorn src.main:app --reload --port 8000`

### Frontend Setup
1. Navigate to frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Visit `http://localhost:3000` in your browser

## Database Schema

The following tables will be created automatically:
- `conversations` - Stores conversation metadata
- `messages` - Stores individual chat messages
- `users` - User authentication data (via Better Auth)

## API Endpoints

- `POST /api/{user_id}/chat` - Send a message and receive AI response
  - Requires JWT authentication
  - Creates new conversation if no conversation_id provided
  - Appends to existing conversation if conversation_id provided

## Key Features

1. **Stateless Architecture**: No session state stored between requests
2. **Database-Driven Context**: Conversation context rebuilt from database on each request
3. **Secure Authentication**: JWT-based authentication with user isolation
4. **Persistent Storage**: All messages and conversations stored in database
5. **Real-time UI**: OpenAI ChatKit integration for smooth user experience

## Development Workflow

1. Run database migrations to create required tables
2. Implement API endpoints following the OpenAPI specification
3. Build AI service that retrieves conversation history from database
4. Create frontend components using OpenAI ChatKit
5. Test stateless behavior by restarting backend during conversations