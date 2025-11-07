# app/api/api_v1/api.py/endpoints/
from fastapi import APIRouter

router = APIRouter()

@router.get('/world')
def say_hello():
  return {"message":"Hello World from SynapseAI modular structure!"}