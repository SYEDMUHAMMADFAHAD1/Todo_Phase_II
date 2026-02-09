# Deployment Guide for Todo Application Backend

This document explains how to deploy the Todo application backend on various platforms.

## Overview

The Todo application consists of:
- Backend: FastAPI application in the `backend/` directory
- Frontend: React application in the `frontend/` directory (separate deployment)

## Backend Deployment on Railway

### Prerequisites

1. A Railway account
2. The repository connected to Railway
3. Environment variables configured (see below)

### Environment Variables

Set these environment variables in your Railway dashboard:

```
DATABASE_URL=postgresql://username:password@host:port/database_name
SECRET_KEY=your-super-secret-jwt-signing-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

For development/testing, you can use SQLite:
```
DATABASE_URL=sqlite:///./todo_app.db
```

### Deployment Steps

1. Push your code to the connected GitHub repository
2. Railway will automatically detect this as a Python application
3. It will use the `Procfile` in the root directory to start the application
4. The application will be deployed using the command:
   ```
   cd backend && python -c "from src.main import app; import uvicorn; import os; port=int(os.environ.get('PORT', 8000)); uvicorn.run(app, host='0.0.0.0', port=port)"
   ```
5. Add the required environment variables in the Railway dashboard
6. Restart the application after setting environment variables

### Alternative Deployment Method

If the main Procfile doesn't work, you can use the alternative:

1. Rename `Procfile.alt` to `Procfile` in your branch
2. Follow the same deployment steps

Or use the start script method:

1. Rename the current `Procfile` and restore the original:
   ```
   web: python start_server.py
   ```
2. This will use the `start_server.py` script in the root directory

## Deployment using Nixpacks

The application also supports deployment using Nixpacks. A `nixpacks.toml` file is included in the root directory with the following configuration:

```toml
[build]
builder = "NIXPACKS"
buildCommand = "cd backend && pip install -r requirements.txt"

[phases.setup]
nixPkgs = ["python313", "pip", "nodejs"]

[phases.build]
cmds = ["cd backend && pip install -r requirements.txt"]

[phases.start]
cmd = "cd backend && uvicorn src.main:app --host=0.0.0.0 --port $PORT"

[variables]
PYTHON_VERSION = "3.13"
```

Platforms that support Nixpacks (such as Render, Fly.io, or other cloud providers) will automatically use this configuration.

### Troubleshooting

#### Common Issues:

1. **Import errors**: Make sure you're in the backend directory when importing modules
2. **Port binding**: The application will use the PORT environment variable provided by the hosting platform
3. **Database connection**: Ensure DATABASE_URL is properly configured for production databases

#### Checking Logs:

View application logs in the dashboard of your hosting platform to troubleshoot startup issues.

### Health Check

Once deployed, you can check the health of your application at:
```
GET /health
```

This endpoint returns `{"status": "ok"}` when the application is running properly.

### API Documentation

After deployment, interactive API documentation is available at:
- `/docs` - Swagger UI
- `/redoc` - ReDoc documentation