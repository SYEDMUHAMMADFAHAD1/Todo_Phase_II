from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback
import logging

from .api.routers import tasks, auth, chat
from .core.config import settings
from .core.db import init_db
from .mcp.server import get_mcp_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Add middleware to log all requests/responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Middleware error for {request.url.path}: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        raise

# Add exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception for {request.url.path}: {exc}", exc_info=True)
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# Add CORS middleware BEFORE routes
# Origins are configurable via CORS_ORIGINS env var (comma-separated)
cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}", tags=["auth"])
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}", tags=["tasks"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}", tags=["chat"])


@app.on_event("startup")
async def startup_event():
    await init_db()
    # Initialize the MCP server
    mcp_server = get_mcp_server()
    print("MCP Server initialized and tools registered")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
