# app/api/api_v1/endpoints/items.py
from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_item():
  return {"item_id": 123, "name": "AI Bot"}