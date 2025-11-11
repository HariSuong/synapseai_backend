# app/api/api_v1/endpoints/items.py
from fastapi import APIRouter, Path, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import item as item_modal
from app.schemas import item as item_schema
from app.crud import crud_item
from app.api.deps import get_db, common_pagination_params



router = APIRouter()

@router.get('/', response_model= list[item_schema.Item])
def get_items(
  pagination: dict = Depends(common_pagination_params),
  db:Session = Depends(get_db)
):
  """
    Lấy danh sách items với phân trang (skip, limit).
    response_model sẽ tự động convert list[dict] này
    thành list[Item] và lọc theo schema 'Item'.
  """
  return crud_item.get_items(db, skip=pagination["skip"], limit=pagination["limit"])
 
@router.post('/', response_model=item_schema.Item, status_code=201)
def create_item(item_in: item_schema.ItemCreate, db:Session = Depends(get_db)):
  
  return crud_item.create_item(db=db, item_in=item_in)

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
  db_item = crud_item.get_item_by_id(db, item_id=item_id)
  if db_item is None:
    raise HTTPException(status_code=404, detail="Item not found!")
  return db_item