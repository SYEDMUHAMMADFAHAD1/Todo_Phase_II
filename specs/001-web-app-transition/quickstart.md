# Developer Quickstart

## Prerequisites
- Node.js 20+
- Python 3.12+
- Neon Postgres Account (or local Postgres)

## 1. Environment Setup

Create a `.env` file in the root (shared by monorepo tools) or separate `.env` files in `backend/` and `frontend/`.

```bash
# Database (Used by Backend and Better Auth)
DATABASE_URL="postgresql+asyncpg://user:pass@host/db?ssl=require"

# Authentication
BETTER_AUTH_SECRET="your-secure-random-secret"
BETTER_AUTH_URL="http://localhost:3000" # Frontend URL

# API
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

## 2. Backend Setup (FastAPI)

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload
```

## 3. Frontend Setup (Next.js)

```bash
cd frontend
npm install
npm run dev
```

## 4. Testing

**Backend**:
```bash
cd backend
pytest
```

**Frontend**:
```bash
cd frontend
npm run test
```
