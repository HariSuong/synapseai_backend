# app/core/email.py (FILE MỚI)

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from app.core.config import settings # Import config "xịn"
import logging

# (A) Cấu hình kết nối SMTP (đọc từ settings)
conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_FROM_NAME = settings.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,  # Bắt buộc cho Gmail port 587
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

# (B) Hàm gửi mail "chung"
async def send_email(email_to: EmailStr, subject: str, body: str):
    """
    Hàm helper để gửi email.
    Nó là hàm 'async' vì fastapi-mail chạy bất đồng bộ.
    """
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],  # Danh sách người nhận
        body=body,
        subtype=MessageType.html  # Gửi dạng HTML
    )
    
    fm = FastMail(conf)
    try:
        # (C) Dùng 'await' vì đây là hàm async
        await fm.send_message(message)
        logging.info(f"Email sent to {email_to}")
    except Exception as e:
        # (D) Bắt lỗi nếu gửi mail thất bại
        logging.error(f"Failed to send email to {email_to}: {e}")

# (E) Hàm tạo nội dung mail chào mừng
async def send_welcome_email(email_to: EmailStr, username: str):
    """
    Tạo nội dung và gửi mail chào mừng.
    """
    subject = f"Chào mừng {username} đến với SynapseAI!"
    
    # Trong dự án thật, em sẽ dùng Jinja2 templates (giống EJS/Handlebars)
    # Tạm thời, chúng ta dùng f-string với HTML
    body = f"""
    <html>
        <head>
            <style>
                body {{ font-family: 'Arial', sans-serif; }}
                .container {{ padding: 20px; }}
                .header {{ font-size: 24px; color: #4CAF50; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="header">Chào mừng, {username}!</h2>
                <p>Cảm ơn bạn đã đăng ký tài khoản tại SynapseAI.</p>
                <p>Chúng ta sẽ cùng nhau xây dựng một dự án SaaS AI tuyệt vời bằng FastAPI và Next.js!</p>
                <br>
                <p>Trân trọng,</p>
                <p><b>Mentor SynapseAI</b></p>
            </div>
        </body>
    </html>
    """
    
    await send_email(email_to=email_to, subject=subject, body=body)