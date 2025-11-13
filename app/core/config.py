# app/core/config.py

# (A) Khóa bí mật để "ký" JWT
SECRET_KEY = "164d4f0bc4c510dc0606672ec5a7b66e80dde0bca29646ee5c6f375377952cfc"

# (B) Thuật toán ký
ALGORITHM = "HS256"

# (C) Thời gian hết hạn của Access Token (30 phút)
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# app/core/config.py (NÂNG CẤP HOÀN TOÀN)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Class này sẽ tự động đọc các biến từ file .env
    """
    
    # Đọc từ file .env (phải chạy pip install pydantic-settings)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # BIẾN BẢO MẬT (Module 7)
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # BIẾN EMAIL (Module 9)
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

# (A) Khởi tạo 1 thể hiện (instance) duy nhất của Settings
# Mọi file khác trong dự án sẽ import `settings` từ file này
settings = Settings()