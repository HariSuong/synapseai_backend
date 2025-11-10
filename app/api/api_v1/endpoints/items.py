# app/api/api_v1/endpoints/items.py
from fastapi import APIRouter, Path, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import item as item_modal
from app.schemas import item as item_schema
from app.api.deps import get_db


router = APIRouter()

@router.get('/', response_model= list[item_schema.Item])
def get_items(
  skip: int = Query(0 , ge=0), # ge=0 (lớn hơn hoặc bằng 0)
  limit: int = Query(10, ge=1, le=50), # ge=1 (>=1), le=50 (<=50)
  db:Session = Depends(get_db)
):
  """
    Lấy danh sách items với phân trang (skip, limit).
    response_model sẽ tự động convert list[dict] này
    thành list[Item] và lọc theo schema 'Item'.
  """
  return db.query(item_modal.Item).offset(skip).limit(limit).all()

@router.post('/', response_model=item_schema.Item, status_code=201)
def create_item(item_in: item_schema.ItemCreate, db:Session = Depends(get_db)):
  """
  Tạo một item mới.
  - item_in: Dữ liệu nhận vào (Request Body), được
              validate (xác thực) bằng schema 'ItemCreate'.
  """
  
  db_item = item_modal.Item(
    description=item_in.description,
    name= item_in.name,
    price=item_in.price 
  )
  
  db.add(db_item)
  db.commit()
  db.refresh(db_item)
  return db_item

@router.get("/{item_id}", response_model=item_schema.Item)
def get_item_by_id(
  item_id :int = Path(
    ...,  # Bắt buộc
    ge=1, # Phải là số nguyên dương
    description="ID của item cần lấy."
  ),
  db:Session = Depends(get_db)
):
  # Tên 'item_id' phải khớp với '{item_id}' trên path
  item_db =  db.query(item_modal.Item).filter(item_modal.Item.id == item_id).first()
  if item_db is None:
    raise HTTPException(status_code=404, detail="Item not found!")
  return item_db