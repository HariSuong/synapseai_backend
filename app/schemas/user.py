# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
  email: EmailStr
  is_active: bool = True
  # Giả sử sau này có thêm:
  # full_name: Optional[str] = None
class UserUpdate(BaseModel):
  """
  Schema dùng khi UPDATE user.
  Tất cả các trường đều là Optional.
  """
  email: Optional[EmailStr] = None
  is_active: Optional[bool] = None
  password: Optional[str] = None # Cho phép đổi pass

class UserCreate(UserBase):
  password: str
  pass

class User(UserBase):
  id: int

  class Config:
    from_attributes = True
