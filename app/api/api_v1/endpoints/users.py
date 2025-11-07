# app/api/api_v1/api.py
from fastapi import APIRouter
from app.schemas import user

router = APIRouter()

@router.post('/', response_model=user.User, status_code=201)
def create_user(user_in: user.UserCreate):
  # Logic "giả" của chúng ta:
  # Em trả về 1 dict khớp với response_model (user.User)
  
  # Sửa lỗi cú pháp (dùng string cho key)
  # Và trả về đủ các trường trong User (id, email, is_active)
  
  new_user_data = {
      "id": 1, 
      "email": user_in.email,         # Lấy từ input
      "is_active": user_in.is_active  # Lấy từ input
  }
  return new_user_data