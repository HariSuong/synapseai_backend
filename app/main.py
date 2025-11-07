from fastapi import FastAPI
from app.api.api_v1.api import api_route

app = FastAPI(
    title="SynapseAI SaaS API",
    description="API cho hệ thống SynapseAI, hỗ trợ multi-tenant và tích hợp AI.",
    version="0.1.0"
)


@app.get('/', tags = ["Root"])
def read_root():
  return {"message": "Welcome to SynapseAI API v1"}

app.include_router(api_route, prefix="/api/v1")