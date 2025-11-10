# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# (A) Chuỗi kết nối (Connection String)
# Cú pháp: "postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME"
# Tạm thời dùng 1 file SQLite cho dễ (Module 18 sẽ đổi qua Supabase/Postgres)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/synapseai"
SQLALCHEMY_DATABASE_URL = "sqlite:///./synapseai.db" # (B)

# (C) Tạo Engine (Động cơ)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # (D) Cần thiết cho SQLite, không cần cho Postgres
    connect_args={"check_same_thread": False} 
)

# (E) Tạo một "nhà máy" sản xuất Session (Session factory)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# (F) Tạo "Class Cha" cho các Model
# Tất cả các model (models/user.py, models/item.py) sẽ kế thừa từ class này
Base = declarative_base()


