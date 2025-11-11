# app/api/api_v1/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.api.deps import get_db
from app.crud import crud_user
from app.schemas import token as token_schema # (B)
from app.core import security
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post('/login', response_model=token_schema.Token)
def login_for_access_token(
  db: Session = Depends(get_db),
  form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint đăng nhập.
    Nhận form data (username, password), trả về JWT.
    """
    # (E) Xác thực user
    # Chú ý: OAuth2 bắt buộc trường tên là "username",
    # nên ta dùng form_data.username, nhưng giá trị là email.
    user = crud_user.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # (F) Tạo Access Token
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, # "sub" (subject) là email
        expires_delta=expires_delta
    )

    # (G) Trả về token cho client
    return {"access_token": access_token, "token_type": "bearer"}