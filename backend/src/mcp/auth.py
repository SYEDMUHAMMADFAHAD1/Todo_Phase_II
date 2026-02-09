"""
JWT Authentication Middleware for MCP Tools

This module provides JWT validation for MCP tools to ensure proper authentication.
"""
from typing import Optional
from fastapi import HTTPException, status, Request
from backend.auth import verify_token, AuthError


def validate_jwt_token(authorization_header: str) -> Optional[dict]:
    """
    Validate the JWT token from the authorization header.
    
    Args:
        authorization_header: The Authorization header value (e.g. "Bearer <token>")
        
    Returns:
        The decoded token payload if valid, None otherwise
    """
    if not authorization_header:
        return None
    
    # Extract the token from the header (remove "Bearer " prefix)
    try:
        if authorization_header.startswith("Bearer "):
            token = authorization_header[7:]
        else:
            token = authorization_header
        
        # Verify the token
        payload = verify_token(token)
        return payload
    except AuthError as e:
        # Token is invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {e.message}"
        )
    except Exception as e:
        # Other error occurred
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}"
        )


def get_user_id_from_token(authorization_header: str) -> str:
    """
    Extract the user ID from the JWT token.
    
    Args:
        authorization_header: The Authorization header value (e.g. "Bearer <token>")
        
    Returns:
        The user ID if valid, raises HTTPException otherwise
    """
    payload = validate_jwt_token(authorization_header)
    
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing subject claim"
        )
    
    return str(payload["sub"])