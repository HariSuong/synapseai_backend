from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.database import engine
from app import models

# (1) Import cả engine VÀ Base từ app.database
from app.database import engine, Base 
from app import models # (2) Vẫn import models (để đăng ký)

# (3) Sửa models.Base thành Base (vì ta import trực tiếp)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SynapseAI SaaS API",
    description="API cho hệ thống SynapseAI, hỗ trợ multi-tenant và tích hợp AI.",
    version="0.1.0"
)


@app.get('/', tags = ["Root"])
def read_root():
  return {"message": "Welcome to SynapseAI API v1"}

app.include_router(api_router, prefix="/api/v1")