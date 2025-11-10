# app/schemas/item.py

from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
  name: str
  description: Optional[str] = None
  price: float

class ItemCreate(ItemBase):
  pass

class Item(ItemBase):
  id: int

  class Config:
    from_attributes = True
  
