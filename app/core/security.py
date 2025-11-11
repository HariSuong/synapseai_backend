# app/core/security.py
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from typing import Optional
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# (A) Khởi tạo "context" băm, nói cho nó biết ta dùng bcrypt
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Kiểm tra mật khẩu gốc có khớp với mật khẩu đã băm không.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Băm mật khẩu gốc.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Tạo ra Access Token (JWT).
    """
    to_encode = data.copy()
    
    # (B) Thiết lập thời gian hết hạn
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:    
        # Hết hạn sau 15 phút nếu không chỉ định
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)    
    
    to_encode.update({"exp" : expire})    

    # (C) Ký và tạo token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[str]:
    """
    Giải mã token, trả về 'subject' (email/id) nếu hợp lệ.
    """

    try:  
      # (D) Giải mã
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

      # (E) Lấy 'sub' (subject) từ payload
      sub = payload.get("sub")
      if sub is None:
          return None # Token hợp lệ nhưng không có 'sub'
      return sub
    except JWTError:
      # (F) Token không hợp lệ (hết hạn, chữ ký sai...)        
      return None