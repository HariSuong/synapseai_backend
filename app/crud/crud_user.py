# app/crud/crud_user.py
from sqlalchemy.orm import Session
from app.models import user as user_model
from app.schemas import user as user_schema

def get_user_by_id(db: Session, user_id: int):
    """
    Service (CRUD) để lấy user bằng ID.
    Đây là logic DB thuần túy.
    """
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Service (CRUD) để lấy user bằng email.
    """
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Service (CRUD) để lấy danh sách user.
    """
    return db.query(user_model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user_in: user_schema.UserCreate):
    """
    Service (CRUD) để tạo user mới.
    """
    # (Chúng ta sẽ hash pass thật ở Module 7)
    fake_hashed_password = user_in.password + "_not_hashed"
    
    db_user = user_model.User(
        email=user_in.email,
        hashed_password=fake_hashed_password,
        is_active=user_in.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Em có thể tự viết:
# def update_user(...): ...
# def delete_user(...): ...