from pydantic import BaseModel, Field
from typing import Optional


class DirectorCreateRequest(BaseModel):
    """درخواست ایجاد کارگردان"""
    name: str = Field(..., min_length=1, max_length=255, description="نام کارگردان")
    birth_year: Optional[int] = Field(None, ge=1800, le=2100, description="سال تولد")
    description: Optional[str] = Field(None, max_length=5000, description="توضیحات")


class DirectorUpdateRequest(BaseModel):
    """درخواست به‌روزرسانی کارگردان"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    birth_year: Optional[int] = Field(None, ge=1800, le=2100)
    description: Optional[str] = Field(None, max_length=5000)
