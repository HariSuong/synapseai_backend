# app/api/deps.py
from fastapi import Query
from sqlalchemy.orm import Session
from app.database import SessionLocal

def get_db():
    """
    Dependency (phụ thuộc) để tạo ra một DB Session
    cho mỗi request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def common_pagination_params(
    skip: int = Query(0, ge=0, description="Số lượng bỏ qua"),
    limit: int = Query(50, ge=1, le=100, description="Số lượng tối đa")
):
    """
    Một dependency dùng chung cho các tham số phân trang (skip, limit).
    """
    # (C) Hàm này chỉ trả về một dict
    return {"skip": skip, "limit": limit}        