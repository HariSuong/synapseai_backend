# app/api/api_v1/endpoints/uploads.py
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from typing import List
import shutil         # (A) Thư viện "Shell Utils" để copy file
from pathlib import Path # (B) Thư viện để xử lý đường dẫn file

from app.api.deps import get_current_user
from app.models import user as user_model

router = APIRouter()

# (C) Nơi lưu file (Tạm thời là local)
# Path() sẽ tự động xử lý dấu "/" hay "\" cho OS
UPLOAD_DIRECTORY = Path("./static/uploads/")
# Tạo thư mục nếu nó chưa tồn tại
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


@router.post("/avatar")
def upload_user_avatar(
    file: UploadFile, # (D) Dùng UploadFile, KHÔNG phải File
    current_user: user_model.User = Depends(get_current_user) # (E)
):
    """
    Upload ảnh avatar cho user đang đăng nhập.
    User phải gửi token (đã học ở Module 7)
    """
    
    # (F) Validate file type (luôn luôn làm)
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="File không hợp lệ. Chỉ chấp nhận .jpg hoặc .png"
        )

    # (G) Tạo đường dẫn lưu file an toàn
    # Chúng ta sẽ lưu file với tên là user_id (ví dụ: 1.png)
    # Lấy đuôi file (ví dụ: .png)
    file_extension = Path(file.filename).suffix 
    file_name = f"{current_user.id}{file_extension}"
    file_location = UPLOAD_DIRECTORY / file_name
    
    # (H) Logic Stream: Đọc chunk và ghi ra đĩa
    try:
        # Mở file trên đĩa ở chế độ "write binary" (wb)
        with file_location.open("wb") as buffer:
            # copyfileobj sẽ đọc 'file.file' (stream) từng mẩu (chunk)
            # và ghi (write) vào 'buffer'
            shutil.copyfileobj(file.file, buffer)
    finally:
        # (I) Luôn luôn đóng stream của file
        file.file.close()

    # (J) Trả về thông tin file đã lưu
    # (Sau này em có thể lưu đường dẫn file_location vào cột avatar_url trong DB)
    return {
        "info": f"File '{file_name}' đã được lưu cho user {current_user.email}",
        "saved_location": str(file_location)
    }


@router.post("/documents")
def upload_multiple_documents(
    files: List[UploadFile], # (K) Dùng List[UploadFile]
    current_user: user_model.User = Depends(get_current_user)
):
    """
    Upload NHIỀU file tài liệu (PDF) cùng lúc.
    Đây là tính năng để nạp kiến thức cho SynapseAI.
    """
    saved_files = []
    for file in files:
        if file.content_type != "application/pdf":
            # Bỏ qua file không phải PDF
            print(f"Bỏ qua file {file.filename}: không phải PDF")
            continue

        file_location = UPLOAD_DIRECTORY / file.filename
        
        # Dùng 'with' sẽ tự động đóng file (buffer)
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file.file.close() # Vẫn phải đóng file upload stream
        saved_files.append(file.filename)
    
    return {
        "message": f"Đã lưu thành công {len(saved_files)} file PDF.",
        "saved_files": saved_files
    }

