from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

from auth import get_current_user as get_current_user_from_auth
from auth import UserIdentity

# Import the authentication function from the main auth module
get_current_user = get_current_user_from_auth