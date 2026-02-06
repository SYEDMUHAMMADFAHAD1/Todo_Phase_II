# Authentication module for FastAPI
# Implements JWT verification and user extraction

import os
import jwt
from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Security Scheme for OpenAPI
security = HTTPBearer()

# Configuration
ALGORITHM = "HS256"

class UserIdentity(BaseModel):
    """
    User context extracted from JWT.
    Note: 'sub' claim maps to 'id'.
    """
    id: str
    email: Optional[str] = None
    name: Optional[str] = None

class AuthError(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        self.message = message
        self.status_code = status_code

def verify_token(token: str) -> dict:
    """
    Verifies the JWT signature and expiration.

    Args:
        token: The encoded JWT string.

    Returns:
        The decoded payload as a dictionary.

    Raises:
        AuthError: If token is invalid, expired, or missing secret.
    """
    # Always check os.environ to support tests modifying the environment
    secret = os.getenv("BETTER_AUTH_SECRET")

    if not secret:
        # Critical configuration error - usually should be 500, but failing auth is safer
        raise AuthError(
            message="Server configuration error: Missing auth secret",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        # Better Auth typically uses HS256 for shared secrets
        payload = jwt.decode(
            token,
            secret,
            algorithms=[ALGORITHM],
            options={"verify_exp": True}
        )

        # Validate required 'sub' claim
        if "sub" not in payload:
            raise AuthError(message="Authentication failed: Missing subject claim")

        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError(message="Token has expired")
    except jwt.InvalidTokenError:
        raise AuthError(message="Invalid token")
    except AuthError:
        raise
    except Exception as e:
        raise AuthError(message=f"Authentication failed: {str(e)}")

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(security)]
) -> UserIdentity:
    """
    FastAPI dependency to extract and verify the user from the Bearer token.

    Usage:
        @app.get("/items")
        def read_items(user: Annotated[UserIdentity, Depends(get_current_user)]):
            ...
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = verify_token(credentials.credentials)

        # Extract user identity
        # The 'sub' claim is the standard JWT subject (user ID)
        user_id = payload.get("sub")
        if not user_id:
            raise AuthError(message="Token missing subject claim")

        return UserIdentity(
            id=str(user_id),  # Ensure user_id is converted to string
            email=payload.get("email"),
            name=payload.get("name")
        )

    except AuthError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
