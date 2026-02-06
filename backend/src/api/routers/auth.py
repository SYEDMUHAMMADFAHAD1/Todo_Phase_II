from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, EmailStr
import jwt
from typing import Optional, Annotated
from passlib.context import CryptContext

from backend.auth import UserIdentity, get_current_user
from backend.src.core.config import settings
from backend.src.core.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.task import User
from sqlalchemy import select

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class SessionResponse(BaseModel):
    user: dict
    session: dict
    token: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    import time
    to_encode = data.copy()
    if expires_delta:
        expire = expires_delta
    else:
        expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire_timestamp = time.time() + expire.total_seconds()
    to_encode.update({"exp": expire_timestamp})
    encoded_jwt = jwt.encode(to_encode, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

@router.post("/auth/signin", response_model=SessionResponse)
async def sign_in(
    request: SignInRequest,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Sign in endpoint that authenticates user and returns session data."""
    # Find user by email
    result = await session.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "name": user.name or ''},
        expires_delta=access_token_expires
    )

    # Prepare session response
    import time
    expires_at_timestamp = time.time() + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    session_data = {
        "id": str(user.id) + "_session",  # Generate a session ID
        "userId": str(user.id),
        "expiresAt": str(expires_at_timestamp),
        "createdAt": str(user.created_at) if hasattr(user, 'created_at') else str(int(time.time()))
    }

    return SessionResponse(
        user={
            "id": str(user.id),
            "email": user.email,
            "name": user.name or '',
            "createdAt": str(user.created_at) if hasattr(user, 'created_at') else str(int(time.time())),
            "updatedAt": str(user.updated_at) if hasattr(user, 'updated_at') else str(int(time.time())),
        },
        session=session_data,
        token=access_token
    )


@router.post("/auth/signup", response_model=SessionResponse)
async def sign_up(
    request: SignUpRequest,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Sign up endpoint that creates a new user and returns session data."""
    # Check if user already exists
    result = await session.execute(select(User).where(User.email == request.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    # Hash the password
    hashed_password = get_password_hash(request.password)

    # Create new user
    new_user = User(
        email=request.email,
        name=request.name,
        password=hashed_password
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_user.id), "email": new_user.email, "name": new_user.name or ''},
        expires_delta=access_token_expires
    )

    # Prepare session response
    import time
    expires_at_timestamp = time.time() + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    session_data = {
        "id": str(new_user.id) + "_session",  # Generate a session ID
        "userId": str(new_user.id),
        "expiresAt": str(expires_at_timestamp),
        "createdAt": str(new_user.created_at) if hasattr(new_user, 'created_at') else str(int(time.time()))  # Simplified
    }

    return SessionResponse(
        user={
            "id": str(new_user.id),
            "email": new_user.email,
            "name": new_user.name or '',
            "createdAt": str(new_user.created_at) if hasattr(new_user, 'created_at') else str(int(time.time())),
            "updatedAt": str(new_user.updated_at) if hasattr(new_user, 'updated_at') else str(int(time.time())),
        },
        session=session_data,
        token=access_token
    )


@router.post("/auth/signout")
async def sign_out():
    """Sign out endpoint."""
    # In a real implementation, you might invalidate the token
    # For now, just return success
    return {"message": "Successfully signed out"}


@router.get("/auth/session", response_model=SessionResponse)
async def get_session(
    request: Request,  # Need to access the request to get the token
    current_user: Annotated[UserIdentity, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """Get current session information."""
    # Get user details from database
    result = await session.execute(select(User).where(User.id == current_user.id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    import time
    expires_at_timestamp = time.time() + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    # Create a session representation
    session_data = {
        "id": str(current_user.id) + "_session",  # Ensure ID is string
        "userId": str(current_user.id),  # Ensure userId is string
        "expiresAt": str(expires_at_timestamp),
        "createdAt": str(user.created_at) if hasattr(user, 'created_at') else str(int(time.time()))
    }

    # Extract token from authorization header to return to frontend
    auth_header = request.headers.get("authorization")
    token = ""
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[len("Bearer "):]

    return SessionResponse(
        user={
            "id": current_user.id,
            "email": current_user.email or user.email,
            "name": current_user.name or user.name or "",
            "createdAt": str(user.created_at) if hasattr(user, 'created_at') else str(int(time.time())),
            "updatedAt": str(user.updated_at) if hasattr(user, 'updated_at') else str(int(time.time())),
        },
        session=session_data,
        token=token
    )