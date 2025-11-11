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
def update_user(db: Session, db_user: user_model.User, user_in: user_schema.UserUpdate ): 
    """
    Service (CRUD) để cập nhật user.
    Đây là logic DB thuần túy.
    """
    # (A) Lấy dict chỉ chứa các trường được gửi lên
    update_data = user_in.model_dump(exclude_unset=True)

    # (B) Logic hash pass (nếu có)
    if "password" in update_data:
        fake_hashed_password = update_data["password"] + "_not_hashed"
        # Ghi đè (overwrite) plain-text pass bằng pass đã hash
        update_data["hashed_password"] = fake_hashed_password
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