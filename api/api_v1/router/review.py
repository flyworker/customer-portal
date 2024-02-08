from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.user_has_role import User
from schema.review import ReviewCreate
from core.token import get_current_user
from service.review import ReviewService

router = APIRouter(prefix="/review", tags=["Review"])


@router.get("/")
def getAllReview(db: Session = Depends(get_db)):
    return ReviewService.get_all(db=db)


@router.post("/create/{productid}")
def createReview(
    productid: int,
    request: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(request)
    print(productid)
    return ReviewService.create_review(
        request=request, productId=productid, db=db, current_user=current_user
    )


@router.post("/coba")
def cobaReview(request: ReviewCreate):
    return request

