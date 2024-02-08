
from fastapi import APIRouter
from api.api_v1.router import product as product_router, user as users_router, auth as auth_router, \
    order as order_router, review as review_router, role

api_router = APIRouter()

api_router.include_router(auth_router.router)
api_router.include_router(users_router.router)
api_router.include_router(review_router.router)
api_router.include_router(product_router.router)
api_router.include_router(order_router.router)
api_router.include_router(role.router)
