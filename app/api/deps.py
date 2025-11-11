# app/api/deps.py
from fastapi import Query, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal

from app.models import user as user_model
from app.crud import crud_user
from app.core import security

# Khởi tạo "người gác cổng"
# Nó biết rằng nó phải lấy token từ URL "/api/v1/auth/login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

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
    #  Hàm này chỉ trả về một dict
    return {"skip": skip, "limit": limit}        


# DEPENDENCY BẢO VỆ
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme) # (D)
) -> user_model.User:
    """
    Dependency "gác cổng":
    1. Lấy token từ header (nhờ oauth2_scheme).
    2. Giải mã token.
    3. Lấy user từ DB.
    4. Trả về user model (nếu hợp lệ).
    """
    # Tạo lỗi 401
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Giải mã token
    email = security.decode_token(token)
    if email is None:
        raise credentials_exception

    # Lấy user từ DB
    user = crud_user.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception # User không tồn tại
        
    # Trả về User model
    return user