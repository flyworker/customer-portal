from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from core.token import create_access_token
from core.database import get_db
from models.user_has_role import Role, User, user_has_role
from core.hashing import Hashing
from sqlalchemy.orm import Session
import logging

app = FastAPI()
router = APIRouter(tags=["Authentication"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/login")
def login(
        request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    logger.info(f"Attempting to login user: {request.username}")

    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        logger.error(f"User with email {request.username} not found!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not Hashing.verify(user.password, request.password):
        logger.error(f"Failed password verification for user: {request.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    # Retrieve user roles
    user_roles = db.query(Role).join(user_has_role).filter(user_has_role.c.user_id == user.id).all()
    role_names = [role.name for role in user_roles]

    logger.info(f"Roles for user {request.username}: {', '.join(role_names)}")

    # Create token
    access_token = create_access_token(data={"sub": user.email, "roles": role_names}, scopes=role_names)

    response = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "jwtToken": access_token,
    }

    return response
