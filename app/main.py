from fastapi import FastAPI, Request
from app.api.api_v1.api import api_router
from app.database import engine
from app import models
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
from app.core.config import settings

# (1) Import cả engine VÀ Base từ app.database
from app.database import engine, Base 
from app import models # (2) Vẫn import models (để đăng ký)

# (3) Sửa models.Base thành Base (vì ta import trực tiếp)
# Base.metadata.create_all(bind=engine)

# (D) Cấu hình logging cơ bản
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

app = FastAPI(
    title="SynapseAI SaaS API",
    description="API cho hệ thống SynapseAI, hỗ trợ multi-tenant và tích hợp AI.",
    version="0.1.0"
)


origins = [
    settings.CLIENT_ORIGIN_DEV,
    settings.CLIENT_ORIGIN_PROD,
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins, # (G) Chỉ cho phép các origin này
  allow_credentials=True, # (H) Cho phép gửi cookie/token
  allow_methods=["*"],    # (I) Cho phép tất cả methods
  allow_headers=["*"],    # (J) Cho phép tất cả headers
)

# (K) Middleware ghi Log và đo lường Performance
@app.middleware("http")
async def add_process_time_header_and_log(request: Request, call_next):
    """
    Middleware này làm 2 việc:
    1. Ghi log cho mỗi request đến.
    2. Đo thời gian xử lý và thêm vào response header "X-Process-Time".
    """
    
    # (L) TRƯỚC khi endpoint chạy
    start_time = time.time()
    
    # Ghi log (giống camera an ninh)
    # Em đã dùng logging.error() ở Module 9, giờ em dùng info()
    log.info(f"Request: {request.method} {request.url.path}")
    
    # (M) Chạy endpoint (giống "next()" trong Express)
    response = await call_next(request)
    
    # (N) SAU khi endpoint chạy xong
    process_time = (time.time() - start_time) * 1000 # Đổi sang miligiây
    
    # (O) Gắn header X-Process-Time vào response
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms" # Làm tròn 2 chữ số
    
    # Ghi log
    log.info(f"Response: {response.status_code} | Process Time: {process_time:.2f}ms")
    
    return response

@app.get('/', tags = ["Root"])
def read_root():
  return {"message": "Welcome to SynapseAI API v1"}

app.include_router(api_router, prefix="/api/v1")