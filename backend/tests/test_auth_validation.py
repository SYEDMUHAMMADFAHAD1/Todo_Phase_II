"""
Unit tests for JWT verification logic.

Tests cover:
- Valid JWT token verification
- Expired token rejection
- Invalid signature rejection
- Missing Authorization header
- Malformed Bearer header
- UserIdentity extraction from claims

These tests validate that backend/auth.py implements secure token verification.
"""

import pytest
from backend.auth import verify_token, get_current_user, AuthError, UserIdentity
from fastapi import HTTPException, status


class TestJWTVerification:
    """Tests for JWT token verification logic"""

    def test_valid_jwt_verification(self, create_valid_jwt):
        """Test that a valid JWT token decodes correctly with expected claims"""
        token = create_valid_jwt(user_id="user-123", email="test@example.com", name="Test User")

        payload = verify_token(token)

        assert payload["sub"] == "user-123"
        assert payload["email"] == "test@example.com"
        assert payload["name"] == "Test User"
        assert "exp" in payload
        assert "iat" in payload

    def test_expired_jwt_verification(self, create_expired_jwt):
        """Test that an expired JWT token raises AuthError with correct message"""
        token = create_expired_jwt(user_id="user-123")

        with pytest.raises(AuthError) as exc_info:
            verify_token(token)

        assert "expired" in str(exc_info.value.message).lower()
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_signature_jwt_verification(self, create_invalid_signature_jwt):
        """Test that a JWT token with invalid signature raises AuthError"""
        token = create_invalid_signature_jwt(user_id="user-123")

        with pytest.raises(AuthError) as exc_info:
            verify_token(token)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid" in str(exc_info.value.message) or "Authentication" in str(exc_info.value.message)

    def test_missing_subject_claim(self):
        """Test that a JWT without 'sub' claim raises AuthError"""
        import jwt
        import os
        from datetime import datetime, timedelta, timezone

        secret = os.getenv("BETTER_AUTH_SECRET")
        payload = {
            "email": "test@example.com",
            # Missing 'sub' claim
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        token = jwt.encode(payload, secret, algorithm="HS256")

        with pytest.raises(AuthError) as exc_info:
            verify_token(token)

        assert "Authentication failed" in str(exc_info.value.message)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


class TestUserIdentityExtraction:
    """Tests for UserIdentity extraction from JWT claims"""

    def test_user_identity_from_valid_token(self, create_valid_jwt):
        """Test that UserIdentity is correctly extracted from JWT claims"""
        token = create_valid_jwt(
            user_id="user-456",
            email="john@example.com",
            name="John Doe"
        )

        payload = verify_token(token)
        user_identity = UserIdentity(
            id=payload.get("sub"),
            email=payload.get("email"),
            name=payload.get("name")
        )

        assert user_identity.id == "user-456"
        assert user_identity.email == "john@example.com"
        assert user_identity.name == "John Doe"

    def test_user_identity_with_optional_claims(self, create_valid_jwt):
        """Test that UserIdentity handles optional claims gracefully"""
        token = create_valid_jwt(user_id="user-789")  # No email, name

        payload = verify_token(token)
        user_identity = UserIdentity(
            id=payload.get("sub"),
            email=payload.get("email"),
            name=payload.get("name")
        )

        assert user_identity.id == "user-789"
        assert user_identity.email is None
        assert user_identity.name is None


class TestErrorHandling:
    """Tests for error handling in JWT verification"""

    def test_missing_secret_configuration(self):
        """Test that missing BETTER_AUTH_SECRET raises AuthError"""
        import os
        import jwt
        from datetime import datetime, timedelta, timezone

        # Temporarily remove secret
        original_secret = os.environ.pop("BETTER_AUTH_SECRET", None)

        try:
            payload = {
                "sub": "user-123",
                "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            }
            token = jwt.encode(payload, "some_secret", algorithm="HS256")

            with pytest.raises(AuthError) as exc_info:
                verify_token(token)

            assert "configuration error" in str(exc_info.value.message).lower()
            assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

        finally:
            # Restore original secret
            if original_secret:
                os.environ["BETTER_AUTH_SECRET"] = original_secret

    def test_malformed_token_handling(self):
        """Test that a malformed token raises AuthError"""
        malformed_token = "not.a.valid.jwt.token"

        with pytest.raises(AuthError) as exc_info:
            verify_token(malformed_token)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


class TestTokenClaims:
    """Tests for JWT token claims and requirements"""

    def test_token_expiration_validation(self, create_valid_jwt, create_expired_jwt):
        """Test that token expiration is properly validated"""
        # Valid token should pass
        valid_token = create_valid_jwt("user-123")
        payload = verify_token(valid_token)
        assert "exp" in payload

        # Expired token should fail
        expired_token = create_expired_jwt("user-123")
        with pytest.raises(AuthError):
            verify_token(expired_token)

    def test_issued_at_claim_present(self, create_valid_jwt):
        """Test that 'iat' (issued at) claim is present in token"""
        token = create_valid_jwt("user-123")
        payload = verify_token(token)

        assert "iat" in payload
        assert isinstance(payload["iat"], int)

    def test_sub_claim_format(self, create_valid_jwt):
        """Test that 'sub' claim contains valid user ID"""
        user_id = "user-secure-id-12345"
        token = create_valid_jwt(user_id=user_id)
        payload = verify_token(token)

        assert payload["sub"] == user_id
        assert len(payload["sub"]) > 0
