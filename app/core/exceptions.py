# app/core/exceptions.py (FILE MỚI)

class SynapseAIException(Exception):
    """
    Lỗi "cha" (base) cho toàn bộ dự án.
    Tất cả lỗi custom nên kế thừa từ đây.
    """
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


# --- Lỗi User (Module 7, 11) ---
class UserNotFoundError(SynapseAIException):
    """Quăng ra khi không tìm thấy user trong DB."""
    def __init__(self, detail: str = "User not found"):
        super().__init__(detail)


class EmailAlreadyExistsError(SynapseAIException):
    """Quăng ra khi đăng ký email đã tồn tại (Module 7)."""
    def __init__(self, detail: str = "Email already registered"):
        super().__init__(detail)        