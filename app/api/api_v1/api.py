# app/api/api_v1/api.py
from fastapi import APIRouter

from app.api.api_v1.endpoints import hello
from app.api.api_v1.endpoints import items

api_route = APIRouter()

api_route.include_router(hello.router, prefix = '/hello', tags=["Hello"])
api_route.include_router(items.router, prefix= '/items', tags=['Item'])
