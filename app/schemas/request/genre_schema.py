from pydantic import BaseModel, Field
from typing import Optional


class GenreCreateRequest(BaseModel):
    """درخواست ایجاد ژانر"""
    name: str = Field(..., min_length=1, max_length=100, description="نام ژانر")
    description: Optional[str] = Field(None, max_length=5000, description="توضیحات")


class GenreUpdateRequest(BaseModel):
    """درخواست به‌روزرسانی ژانر"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=5000)
