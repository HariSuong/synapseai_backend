# app/api/api_v1/api.py
from fastapi import APIRouter

from app.api.api_v1.endpoints import items, users, auth


api_router = APIRouter()


api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(items.router, prefix= '/items', tags=['Item'])
api_router.include_router(users.router, prefix= '/users', tags=['User'])
