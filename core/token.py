from datetime import datetime, timedelta
from typing import List, Optional

from jwt import PyJWTError
import jwt
from sqlalchemy.orm import Session

from fastapi.security import SecurityScopes
from core.database import get_db
from models.user_has_role import User
from service.user import UserService
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Token creation with scopes
def create_access_token(data: dict, scopes: List[str]):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "scopes": scopes})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Verify token with scopes
def verify_token(token: str, credentials_exception, required_scopes: Optional[List[str]] = None,
                 db: Session = Depends(get_db)):
    try:
        # Decoding the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email: str = payload.get("sub")

        # Extract roles from token
        token_roles = payload.get("roles", [])

        # If scopes are specified, check if the user has the required roles
        if required_scopes:
            common_scopes = [scope for scope in required_scopes if scope in token_roles]
            if not common_scopes:
                raise credentials_exception

        if email is None:
            raise credentials_exception

    except PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user


# Get the current user with scope checking
def get_current_user(security_scopes: SecurityScopes, db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    return verify_token(token=token, credentials_exception=credentials_exception,
                        required_scopes=security_scopes.scopes, db=db)
