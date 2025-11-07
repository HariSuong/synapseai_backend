from pydantic import BaseModel, EmailStr
from typing import List

class UserBase(BaseModel):
  emai: EmailStr
  is_active: bool = True
  # Giả sử sau này có thêm:
  # full_name: Optional[str] = None

class UserCreate(UserBase):
  password: str
  pass

class User(UserBase):
  id: int

  class config:
    from_attributes = True
