# app/api/api_v1/endpoints/users.py
from fastapi import APIRouter, Path, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas import user as user_schema
from app.models import user as user_model
from app.api.deps import get_db, common_pagination_params, get_current_user
from app.crud import crud_user
from app.core.email import send_welcome_email

router = APIRouter()



@router.post('/', response_model=user_schema.User, status_code=201)
def create_user(
  user_in: user_schema.UserCreate,
  tasks: BackgroundTasks,
  db:Session = Depends(get_db)
):
   """
   Tạo user mới VÀ gửi mail chào mừng (trong nền)
   """
   # (B) Logic nghiệp vụ của Endpoint
   #      (Tầng API chịu trách nhiệm check lỗi HTTP)
   db_user = crud_user.get_user_by_email(db, email=user_in.email)
   if db_user:
      raise HTTPException(
         status_code=400,
         detail="Email already registered",
      )
   
   # (C) Tạo user trong DB (việc nhanh)
   new_user = crud_user.create_user(db=db, user_in=user_in)

   # (D) Thêm tác vụ gửi mail vào HÀNG ĐỢI
   # Hàm này CHƯA chạy. Nó chỉ chạy SAU KHI "return new_user"
   tasks.add_task(
      send_welcome_email,
      email_to = user_in.email,
      username = user_in.email
   )

   return new_user


@router.get('/', response_model=list[user_schema.User])
def get_users(
   pagination: dict = Depends(common_pagination_params),
   db: Session = Depends(get_db),
   current_user: user_model.User = Depends(get_current_user)
):
  """
  Lấy danh sách users (có phân trang) (YÊU CẦU ĐĂNG NHẬP)
  """
  print(f"User {current_user.email} đang gọi API này.")
  users = crud_user.get_users(db, skip=pagination["skip"], limit=pagination["limit"])
  
  # Trả về list đã lọc (có thể là list rỗng [], chứ không phải None)
  return users


@router.get("/me", response_model=user_schema.User)
def read_users_me(
   current_user: user_model.User = Depends(get_current_user)
):
   """
   Lấy thông tin của user đang đăng nhập (từ token).
   """
   # Không cần query DB nữa, dependency đã làm rồi
   return current_user



@router.get('/{user_id}', response_model=user_schema.User)
def get_user_by_id(user_id : int = Path(..., ge=1), db: Session = Depends(get_db)):
  # Tìm user (chúng ta sẽ làm xịn hơn ở Module 4)
  
  db_user = crud_user.get_user_by_id(db, user_id=user_id)
  
  if db_user is None:
     raise HTTPException(status_code=404, detail="User not found")
  return db_user


@router.put('/{user_id}', response_model=user_schema.User)
def edit_user_by_id(
   user_id: int,
   user_in: user_schema.UserUpdate, # (A) Dùng UserUpdate
   db: Session = Depends(get_db)
):
   """
   Cập nhật user.
   (Tầng API chỉ lo check 404)
   """
   # (B) Tầng API gọi CRUD để lấy user
   db_user = crud_user.get_user_by_id(db, user_id=user_id)
   if db_user is None:
      raise HTTPException(status_code=404, detail="User not found")
   
   # (C) Tầng API gọi CRUD để cập nhật
   # Giao hết logic update (set attr, commit) cho CRUD
   updated_user = crud_user.update_user(db=db, db_user=db_user, user_in=user_in)
   
   return updated_user

     


@router.delete("/{user_id}", status_code=204)
def delete_user_by_id(user_id : int = Path(..., ge=1), db: Session = Depends(get_db)):
  # Tìm user 
  db_user = crud_user.get_user_by_id(db, user_id=user_id)
  if db_user is None:
     raise HTTPException(status_code=404, detail="User not found")
  
  crud_user.delete_user(db, db_user)
  return None

