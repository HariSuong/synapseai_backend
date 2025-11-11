# app/crud/crud_item.py

from sqlalchemy.orm import Session
from app.models import item as item_modal
from app.schemas import item as item_schema


def get_items(
  db:Session, 
  skip: int = 0,
  limit: int = 100
):
  """
  CRUD: Lấy list items.
  Chỉ nhận tham số Python thuần túy.
  """
  return db.query(item_modal.Item).offset(skip).limit(limit).all()
  
def get_item_by_id(
  db: Session, 
  item_id :int
):
  """
  CRUD: Lấy item theo ID.
  Chỉ nhận tham số Python thuần túy.
  """
  return db.query(item_modal.Item).filter(item_modal.Item.id == item_id).first()

def create_item(item_in: item_schema.ItemCreate, db:Session):
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