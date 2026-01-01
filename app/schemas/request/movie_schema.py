from pydantic import BaseModel, Field
from typing import Optional, List


class MovieCreateRequest(BaseModel):
    """درخواست ایجاد فیلم"""
    title: str = Field(..., min_length=1, max_length=255, description="عنوان فیلم")
    director_id: int = Field(..., gt=0, description="شناسه کارگردان")
    release_year: int = Field(..., ge=1800, le=2100, description="سال انتشار")
    cast: Optional[str] = Field(None, max_length=5000, description="بازیگران")
    genres: List[int] = Field(..., min_length=1, description="لیست شناسه‌های ژانر")


class MovieUpdateRequest(BaseModel):
    """درخواست به‌روزرسانی فیلم"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    release_year: Optional[int] = Field(None, ge=1800, le=2100)
    cast: Optional[str] = Field(None, max_length=5000)
    genres: Optional[List[int]] = Field(None, min_length=1)
