# Todo Application Backend

This is the backend service for the Todo application built with FastAPI.

## Deployment on Railway

This application is configured for deployment on Railway.

### Configuration

The following environment variables should be set in Railway:

- `DATABASE_URL`: Database connection string (PostgreSQL recommended for production)
- `SECRET_KEY`: Secret key for JWT token signing
- `ALGORITHM`: Algorithm for JWT encoding (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes (default: 30)

### Deployment Steps

1. Connect your GitHub repository to Railway
2. Create a new Railway project
3. Railway will automatically detect this as a Python application
4. The application will be deployed using the Procfile in the root directory
5. Add the required environment variables in the Railway dashboard
6. Redeploy the application after setting environment variables

### Technical Details

- The application is located in the `backend` directory
- The main application entry point is `backend/src/main.py`
- The start script (`start_server.py`) in the root directory handles changing to the backend directory before starting the server
- The Procfile specifies how to start the application: `python start_server.py`
- Dependencies are listed in `backend/requirements.txt`

### Port Configuration

The application will automatically use the port specified by the `PORT` environment variable provided by Railway, defaulting to 8000 if not set.