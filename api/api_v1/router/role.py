from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from service.role import RoleService

router = APIRouter(prefix="/role", tags=["roles"])


@router.get("/")
def get_roles(db: Session = Depends(get_db)):

    return RoleService.get_roles(db=db)

