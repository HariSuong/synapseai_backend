# app/api/api_v1/endpoints/users.py
from fastapi import APIRouter, Path, Query
from app.schemas import user
from typing import Optional

router = APIRouter()

# (1) Mock DB (Nên để ở trên cùng cho dễ quản lý)
fake_all_users_db = [
    {"id": 1, "email": "active@example.com", "is_active": True},
    {"id": 2, "email": "inactive@example.com", "is_active": False},
]

@router.post('/', response_model=user.User, status_code=201)
def create_user(user_in: user.UserCreate):
  """
  Tạo user mới (logic giả).
  """
  # Logic "giả" của chúng ta:
  # Em trả về 1 dict khớp với response_model (user.User)
  
  # Sửa lỗi cú pháp (dùng string cho key)
  # Và trả về đủ các trường trong User (id, email, is_active)
  
  new_user_data = {
    "id": 3, # Giả sử ID tiếp theo là 3
    "email": user_in.email,
    "is_active": user_in.is_active
  }
  fake_all_users_db.append(new_user_data)
  return new_user_data


@router.get('/', response_model=list[user.User])
def get_users(is_active: Optional[bool] = None):
  """
  Lấy danh sách user, có thể lọc theo is_active.
  """
  
  if is_active is None:
    # Trường hợp 1: Không filter, trả về tất cả
    return fake_all_users_db
  
  # Trường hợp 2: Có filter
  # Dùng list comprehension cho gọn (giống .filter() bên JS)
  filtered_users = [u for u in fake_all_users_db if u["is_active"] == is_active]
  
  # Trả về list đã lọc (có thể là list rỗng [], chứ không phải None)
  return filtered_users


@router.get('/{user_id}', response_model=user.User)
def get_user_by_id(user_id : int = Path(..., ge=1)):
  # Tìm user (chúng ta sẽ làm xịn hơn ở Module 4)
  for u in fake_all_users_db:
      if u["id"] == user_id:
          return u
  
  # (H) Nếu không tìm thấy, chúng ta sẽ học trả 404 ở Module 11
  # Tạm thời trả về một user "ảo" để không vi phạm response_model
  return {"id": user_id, "email": "not_found@example.com", "is_active": False}
