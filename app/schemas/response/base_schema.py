from pydantic import BaseModel
from typing import Any, Dict, Optional, List


class SuccessResponse(BaseModel):
    """شکل پاسخ موفق"""
    status: str = "success"
    data: Any


class ErrorDetail(BaseModel):
    """جزئیات خطا"""
    code: int
    message: str


class ErrorResponse(BaseModel):
    """شکل پاسخ ناموفق"""
    status: str = "failure"
    error: ErrorDetail


class PaginatedResponse(BaseModel):
    """شکل پاسخ صفحه‌بندی شده"""
    page: int
    page_size: int
    total_items: int
    items: List[Any]
