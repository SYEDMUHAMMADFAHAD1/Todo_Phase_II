from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import traceback
import logging
from urllib.parse import urlparse

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

# Add CORS middleware - must be before routes
# Origins are configurable via CORS_ORIGINS env var (comma-separated)
cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
logger.info(f"CORS allowed origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}", tags=["auth"])
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}", tags=["tasks"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}", tags=["chat"])


db_ready = False


@app.on_event("startup")
async def startup_event():
    global db_ready

    # Log DATABASE_URL hostname for debugging (never log credentials)
    try:
        parsed = urlparse(settings.DATABASE_URL)
        logger.info(f"DATABASE_URL scheme={parsed.scheme}, host={parsed.hostname}, db={parsed.path}")
        if parsed.hostname in (None, "host", "localhost") and "asyncpg" in (parsed.scheme or ""):
            logger.error(
                "DATABASE_URL has a placeholder hostname '%s'. "
                "Update the DATABASE_URL env var in Railway with your real Neon connection string: "
                "postgresql+asyncpg://user:pass@ep-xxx.region.aws.neon.tech/dbname?ssl=require",
                parsed.hostname,
            )
    except Exception:
        logger.warning("Could not parse DATABASE_URL for diagnostics")

    # Try DB init with retries — do NOT crash the app if it fails
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            await init_db()
            db_ready = True
            logger.info("Database initialized successfully")
            break
        except Exception as e:
            logger.error(f"Database init attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                await asyncio.sleep(2 * attempt)

    if not db_ready:
        logger.error(
            "DATABASE CONNECTION FAILED — app will start but API routes will not work. "
            "Fix DATABASE_URL in Railway environment variables and redeploy."
        )

    # Initialize the MCP server
    mcp_server = get_mcp_server()
    logger.info("MCP Server initialized and tools registered")


@app.get("/health")
async def health_check():
    return {
        "status": "ok" if db_ready else "degraded",
        "database": "connected" if db_ready else "unavailable",
    }
