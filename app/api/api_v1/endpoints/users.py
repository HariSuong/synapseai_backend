# app/api/api_v1/endpoints/users.py
from fastapi import APIRouter, Path, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas import user as user_schema
from app.models import user as user_model
from app.database import SessionLocal

router = APIRouter()

def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()   



@router.post('/', response_model=user_schema.User, status_code=201)
def create_user(
  user_in: user_schema.UserCreate,
  db:Session = Depends(get_db)
):
  """
  Tạo user mới 
  """
  fake_hashed_password = user_in.password + "_not_hashed"

  # Tạo 1 đối tượng Model (SQLAlchemy) từ
  # dữ liệu của Schema (Pydantic)  
  db_user = user_model.User(
     email = user_in.email,
     hashed_password=fake_hashed_password,
     is_active=user_in.is_active
  )

  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


@router.get('/', response_model=list[user_schema.User])
def get_users(
  skip: int = 0, 
  limit: int = 100, 
  db: Session = Depends(get_db)
):
  """
  Lấy danh sách users (có phân trang)
  """
  
  users = db.query(user_model.User).offset(skip).limit(limit).all()
  
  # Trả về list đã lọc (có thể là list rỗng [], chứ không phải None)
  return users


@router.get('/{user_id}', response_model=user_schema.User)
def get_user_by_id(user_id : int = Path(..., ge=1), db: Session = Depends(get_db)):
  # Tìm user (chúng ta sẽ làm xịn hơn ở Module 4)
  
  db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
  
  if db_user is None:
     raise HTTPException(status_code=404, detail="User not found")
  return db_user


@router.put('/{user_id}', response_model=user_schema.User)
def edit_user_by_id(
   user_id : int,
   user_in: user_schema.UserUpdate,
   db: Session = Depends(get_db)
):
  # Tìm user (chúng ta sẽ làm xịn hơn ở Module 4)
  db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
  if db_user is None:
     raise HTTPException(status_code=404, detail="User not found")
  
  # (C) Lấy dữ liệu từ Pydantic
  # exclude_unset=True: Chỉ lấy các trường mà client
  # *thực sự* gửi lên (bỏ qua các trường None/default)
  update_data = user_in.model_dump(exclude_unset=True)

  if "password" in update_data:
      fake_hashed_password = update_data['password'] + "_not_hashed"
      db_user.hashed_password = fake_hashed_password

  if "email" in update_data:
      db_user.email = update_data["email"]
      
  if "is_active" in update_data:
      db_user.is_active = update_data["is_active"]
  

  db.add(db_user)
  db.commit()
  db.refresh(db_user)

     


@router.delete("/{user_id}", status_code=204)
def delete_user_by_id(user_id : int = Path(..., ge=1), db: Session = Depends(get_db)):
  db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
  if db_user is None:
     raise HTTPException(status_code=404, detail="User not found")
  db.delete(db_user)
  db.commit()
  return None