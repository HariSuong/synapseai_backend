# app/api/api_v1/endpoints/items.py
from fastapi import APIRouter, Path, Query
from app.schemas import item


router = APIRouter()
# Module 4 sẽ thay thế bằng DB thật
fake_items_db = [
    {"id": 1, "name": "AI Bot v1", "description": "Bot v1", "price": 100.0},
    {"id": 2, "name": "AI Bot v2", "description": "Bot v2", "price": 200.0},
    {"id": 3, "name": "AI Bot v3", "description": "Bot v3", "price": 300.0},
]
@router.get('/', response_model= list[item.Item])
def get_items(
  skip: int = Query(0 , ge=0), # ge=0 (lớn hơn hoặc bằng 0)
  limit: int = Query(10, ge=1, le=50) # ge=1 (>=1), le=50 (<=50)
):
  """
    Lấy danh sách items với phân trang (skip, limit).
    response_model sẽ tự động convert list[dict] này
    thành list[Item] và lọc theo schema 'Item'.
  """
  return fake_items_db[skip : skip + limit]

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

@router.get("/items/{item_id}", response_model=item.Item)
def get_item_by_id(
  item_id :int = Path(
    ...,  # Bắt buộc
    ge=1, # Phải là số nguyên dương
    description="ID của item cần lấy."
  )
):
  # Tên 'item_id' phải khớp với '{item_id}' trên path
  for items_db in fake_items_db:
    if items_db["id"] == item_id:
      return items_db
  return None