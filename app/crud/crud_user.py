# app/crud/crud_user.py
from sqlalchemy.orm import Session
from app.models import user as user_model
from app.schemas import user as user_schema
from typing import Optional

from app.core.security import get_password_hash, verify_password

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
    hashed_password = get_password_hash(user_in.password) 
    
    db_user = user_model.User(
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=user_in.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Em có thể tự viết:
def update_user(db: Session, db_user: user_model.User, user_in: user_schema.UserUpdate ): 
    """
    Service (CRUD) để cập nhật user.
    Đây là logic DB thuần túy.
    """
    # (A) Lấy dict chỉ chứa các trường được gửi lên
    update_data = user_in.model_dump(exclude_unset=True)

    # (B) Logic hash pass (nếu có)
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        # Ghi đè (overwrite) plain-text pass bằng pass đã hash
        update_data["hashed_password"] = hashed_password
        # Xóa plain-text pass đi
        del update_data["password"]
    
    # (C) Cập nhật các thuộc tính của object Model
    # db_user là object SQLAlchemy, ta có thể set attr cho nó
    for field in update_data:
        setattr(db_user, field, update_data[field])
    
    # (D) Commit thay đổi
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: user_schema.User):
    db.delete(db_user)
    db.commit()


# (D) HÀM MỚI: Dùng để xác thực
def authenticate_user(db: Session, email: str, password: str) -> Optional[user_model.User]:
    """
    Kiểm tra email và mật khẩu (dùng cho /login).
    """
    # 1. Lấy user bằng email
    user = get_user_by_email(db, email=email)
    if not user:
        return None # User không tồn tại    
    
    # 2. Kiểm tra mật khẩu
    if not verify_password(password, user.hashed_password):
        return None # Sai mật khẩu
    
    # 3. Thành công
    return user




