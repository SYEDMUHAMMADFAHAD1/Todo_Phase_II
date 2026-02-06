"""
Shared test fixtures and configuration for all test files.
Includes JWT token generation and async test client setup.
"""

import pytest
import jwt
import os
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from backend.src.main import app
from backend.src.core.config import settings


# Test Secret Configuration
TEST_SECRET = "test_secret_min_32_chars_long_value"
TEST_ALGORITHM = "HS256"


@pytest.fixture(autouse=True, scope="session")
def setup_test_db():
    """
    Set up test database using in-memory SQLite.
    Runs once per test session.
    """
    import asyncio
    from backend.src.core.db import engine as prod_engine
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    # Create in-memory test database
    test_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )

    # Initialize database tables
    async def init_db():
        async with test_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    asyncio.run(init_db())

    # Override get_session dependency
    async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
        async_session = sessionmaker(
            bind=test_engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            yield session

    from backend.src.core.db import get_session
    app.dependency_overrides[get_session] = get_test_session

    yield

    # Cleanup
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def setup_test_env():
    """
    Set up test environment with test secret.
    Runs automatically before every test.
    """
    original_secret = os.environ.get("BETTER_AUTH_SECRET")
    os.environ["BETTER_AUTH_SECRET"] = TEST_SECRET
    yield
    # Restore original value
    if original_secret is None:
        os.environ.pop("BETTER_AUTH_SECRET", None)
    else:
        os.environ["BETTER_AUTH_SECRET"] = original_secret


# JWT Token Fixtures

@pytest.fixture
def create_valid_jwt():
    """
    Fixture that returns a function to create valid JWT tokens.

    Usage:
        def test_something(create_valid_jwt):
            token = create_valid_jwt("user-123")
            # Use token in test
    """
    def _create_token(user_id: str, email: str = None, name: str = None, hours: int = 1):
        """
        Create a valid JWT token.

        Args:
            user_id: The user ID to encode in "sub" claim
            email: Optional email to encode in "email" claim
            name: Optional name to encode in "name" claim
            hours: Token expiration time in hours (default: 1)

        Returns:
            Encoded JWT token string
        """
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + timedelta(hours=hours),
        }
        if email:
            payload["email"] = email
        if name:
            payload["name"] = name

        return jwt.encode(payload, TEST_SECRET, algorithm=TEST_ALGORITHM)

    return _create_token


@pytest.fixture
def create_expired_jwt():
    """
    Fixture that returns a function to create expired JWT tokens.

    Usage:
        def test_expired_token(create_expired_jwt):
            token = create_expired_jwt("user-123")
            # This token should be rejected with 401
    """
    def _create_token(user_id: str, email: str = None, name: str = None):
        """
        Create an expired JWT token.

        Args:
            user_id: The user ID to encode in "sub" claim
            email: Optional email to encode in "email" claim
            name: Optional name to encode in "name" claim

        Returns:
            Encoded JWT token string (already expired)
        """
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "iat": now - timedelta(hours=2),
            "exp": now - timedelta(hours=1),  # Expired 1 hour ago
        }
        if email:
            payload["email"] = email
        if name:
            payload["name"] = name

        return jwt.encode(payload, TEST_SECRET, algorithm=TEST_ALGORITHM)

    return _create_token


@pytest.fixture
def create_invalid_signature_jwt():
    """
    Fixture that returns a function to create JWT tokens with invalid signature.

    Usage:
        def test_invalid_signature(create_invalid_signature_jwt):
            token = create_invalid_signature_jwt("user-123")
            # This token should be rejected with 401
    """
    def _create_token(user_id: str, email: str = None, name: str = None):
        """
        Create a JWT token with invalid signature (signed with wrong secret).

        Args:
            user_id: The user ID to encode in "sub" claim
            email: Optional email to encode in "email" claim
            name: Optional name to encode in "name" claim

        Returns:
            Encoded JWT token string (signed with wrong secret)
        """
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + timedelta(hours=1),
        }
        if email:
            payload["email"] = email
        if name:
            payload["name"] = name

        # Sign with wrong secret - token will fail verification
        wrong_secret = "wrong_secret_for_testing"
        return jwt.encode(payload, wrong_secret, algorithm=TEST_ALGORITHM)

    return _create_token


# Async Test Client Fixture

@pytest.fixture
async def async_client():
    """
    Fixture that provides an async HTTP client for testing endpoints.

    Usage:
        @pytest.mark.asyncio
        async def test_endpoint(async_client):
            response = await async_client.get("/api/tasks")
            assert response.status_code == 401  # Without auth
    """
    from httpx import ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


# Alternative: AsyncClient with authentication

@pytest.fixture
async def authenticated_async_client(create_valid_jwt):
    """
    Fixture that provides an authenticated async HTTP client.
    Automatically includes valid JWT token in requests.

    Usage:
        @pytest.mark.asyncio
        async def test_authenticated_endpoint(authenticated_async_client):
            response = await authenticated_async_client.get("/api/tasks")
            assert response.status_code == 200  # With valid auth
    """
    from httpx import ASGITransport
    token = create_valid_jwt("test-user-123", email="test@example.com", name="Test User")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Add default Authorization header
        client.headers.update({"Authorization": f"Bearer {token}"})
        yield client


# Database Fixtures (for integration tests if needed)

@pytest.fixture
async def test_db_engine():
    """
    Fixture that provides an async database engine for testing.
    Uses in-memory SQLite for tests (or could use test PostgreSQL).
    """
    # For testing, could use SQLite in-memory: "sqlite+aiosqlite:///:memory:"
    # For now, we'll use test DATABASE_URL from settings
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def test_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture that provides an async database session for tests.
    """
    async_session = sessionmaker(
        bind=test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


# Pytest Configuration

def pytest_configure(config):
    """
    Configure pytest markers for test categorization.
    """
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "contract: mark test as a contract test")
    config.addinivalue_line("markers", "asyncio: mark test as async")
