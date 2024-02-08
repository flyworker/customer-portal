import logging
from typing import Any

from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from constants.role import Role
from core.database import get_db
from models.user_has_role import User
from schema.user import RegisterUser
from service.user import UserService
from core.token import get_current_user
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_all_user(db: Session = Depends(get_db),
                 current_user: User = Security(get_current_user,
                                               scopes=[
                                                   # Role.GUEST["name"],
                                                   Role.ADMIN["name"],
                                                   Role.SUPER_ADMIN["name"],
                                                   Role.ACCOUNT_ADMIN["name"],
                                               ])):
    try:
        logger.info(f"User {current_user.email} with role(s) {current_user.roles} is attempting to retrieve all users.")

        # Here you can implement any other logic you might want, e.g.,
        # checking if the current user has certain permissions beyond just having the correct role.

        users = UserService.get_allUser(db=db)
        logger.info(f"User {current_user.email} successfully retrieved all users.")
        return users
    except Exception as e:
        logger.error(f"An error occurred while user {current_user.email} tried to retrieve all users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/")
def createUser(user: RegisterUser, db: Session = Depends(get_db)):
    return UserService.create_user(user, db)


@router.get("/me")
def getMe(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/{userid}")
def updateUser(userid: int, user: RegisterUser, db: Session = Depends(get_db)):
    return UserService.update_user(userid=userid, user=user, db=db)


@router.delete("/{userid}")
def delete_user(userid: int, db: Session = Depends(get_db)):
    return UserService.deleteUser(userid=userid, db=db)
