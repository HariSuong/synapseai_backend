# app/api/deps.py
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