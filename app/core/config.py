# app/core/config.py

# (A) Khóa bí mật để "ký" JWT
SECRET_KEY = "164d4f0bc4c510dc0606672ec5a7b66e80dde0bca29646ee5c6f375377952cfc"

# (B) Thuật toán ký
ALGORITHM = "HS256"

# (C) Thời gian hết hạn của Access Token (30 phút)
ACCESS_TOKEN_EXPIRE_MINUTES = 30