from sqlalchemy.orm import Session

from models.user_has_role import Role


class RoleService:
    def get_roles(db: Session):
        return db.query(Role).all()
