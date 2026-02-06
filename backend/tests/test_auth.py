# Tests for JWT verification logic

import pytest
import jwt
import os
import datetime
from backend.auth import verify_token, AuthError

# Configuration for testing
TEST_SECRET = "test_secret_123"

@pytest.fixture(autouse=True)
def set_env():
    """Set environment variable for testing"""
    # Save original value if exists
    original_secret = os.environ.get("BETTER_AUTH_SECRET")
    os.environ["BETTER_AUTH_SECRET"] = TEST_SECRET
    yield
    # Restore or delete
    if original_secret is None:
        del os.environ["BETTER_AUTH_SECRET"]
    else:
        os.environ["BETTER_AUTH_SECRET"] = original_secret

def test_verify_valid_token():
    """Test that a valid token decodes correctly"""
    payload = {
        "sub": "user_123",
        "email": "test@example.com",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    encoded = jwt.encode(payload, TEST_SECRET, algorithm="HS256")

    decoded = verify_token(encoded)
    assert decoded["sub"] == "user_123"
    assert decoded["email"] == "test@example.com"

def test_verify_expired_token():
    """Test that an expired token raises AuthError"""
    payload = {
        "sub": "user_123",
        "exp": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)
    }
    encoded = jwt.encode(payload, TEST_SECRET, algorithm="HS256")

    with pytest.raises(AuthError) as excinfo:
        verify_token(encoded)
    assert "expired" in excinfo.value.message.lower()

def test_verify_invalid_signature():
    """Test that a token signed with wrong secret fails"""
    payload = {"sub": "user_123"}
    encoded = jwt.encode(payload, "wrong_secret", algorithm="HS256")

    with pytest.raises(AuthError) as excinfo:
        verify_token(encoded)
    assert "authentication failed" in excinfo.value.message.lower() or "invalid token" in excinfo.value.message.lower()

def test_missing_secret():
    """Test handling of missing configuration"""
    del os.environ["BETTER_AUTH_SECRET"]

    with pytest.raises(AuthError) as excinfo:
        verify_token("some_token")
    assert "configuration error" in excinfo.value.message.lower()
