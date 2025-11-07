# app/api/api_v1/endpoints/items.py
from fastapi import APIRouter
from app.schemas import item
from typing import List
router = APIRouter()
# Module 4 sẽ thay thế bằng DB thật
fake_items_db = [
    {"id": 1, "name": "AI Bot v1", "description": "Bot v1", "price": 100.0},
    {"id": 2, "name": "AI Bot v2", "description": "Bot v2", "price": 200.0},
]
@router.get('/', response_model= List[item.Item])
def get_items():
  """
    Lấy danh sách tất cả items.
    response_model sẽ tự động convert list[dict] này
    thành list[Item] và lọc theo schema 'Item'.
  """
  return fake_items_db

@router.post('/', response_model=item.Item, status_code=201)
def create_item(item_in: item.ItemCreate):
  """
  Tạo một item mới.
  - item_in: Dữ liệu nhận vào (Request Body), được
              validate (xác thực) bằng schema 'ItemCreate'.
  """
  # Tạo một item "giả" với id mới
  new_item_data = item_in.model_dump()
  new_item_id = len(fake_items_db) +1

  new_item = {
    id: new_item_id,
    **new_item_data
  }

  fake_items_db.append(new_item)
  
  # Trả về item vừa tạo, Pydantic sẽ lọc bằng
  # response_model 'Item' (có id)
  return new_item
