from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from starlette import status

from core.database import get_db

from models.user_has_role import User
from sqlalchemy.orm import Session
from schema.user import RegisterUser
from core.hashing import Hashing


class UserService:
    def get_allUser(db: Session):
        return db.query(User).all()

    def get_user(email: str, db: Session = Depends(get_db)):
        return db.query(User).filter(User.email == email).first()

    def create_user(user: RegisterUser, db: Session = Depends(get_db)):
        db_user = User(
            name=user.name,
            email=user.email,
            password=Hashing.bcrypt(user.password),
            is_staff=user.is_staff,
            is_active=user.is_active,
        )

        db.add(db_user)

        try:
            db.commit()
            print("User committed successfully")
            try:
                db.refresh(db_user)
                print("User refreshed successfully")
            except InvalidRequestError as e:
                print(f"Could not refresh the user: {e}")
                return None

        except IntegrityError as e:
            db.rollback()
            print(f"Error occurred during commit: {e}")

            if "unique constraint" in str(e).lower() and "email" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A user with this email already exists."
                )
            return None

        db_user.password = None

        return db_user

    def update_user(userid: int, user: RegisterUser, db: Session):
        db_userid = db.query(User).filter(User.id == userid).first()

        db_userid.name = user.name
        db_userid.email = user.email
        db_userid.password = Hashing.bcrypt(user.password)
        db_userid.is_staff = user.is_staff
        db_userid.is_active = user.is_active

        db.commit()

        return db_userid

    def deleteUser(userid: int, db: Session):
        db_userid = db.query(User).filter(User.id == userid).first()

        db.delete(db_userid)

        db.commit()

        return db_userid
