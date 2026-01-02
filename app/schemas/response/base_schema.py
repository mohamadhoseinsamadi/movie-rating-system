from pydantic import BaseModel
from typing import Any, Dict, Optional, List


class SuccessResponse(BaseModel):
    """Success response format"""
    status: str = "success"
    data: Any


class ErrorDetail(BaseModel):
    """Error details"""
    code: int
    message: str


class ErrorResponse(BaseModel):
    """Failure response format"""
    status: str = "failure"
    error: ErrorDetail


class PaginatedResponse(BaseModel):
    """Paginated response format"""
    page: int
    page_size: int
    total_items: int
    items: List[Any]
