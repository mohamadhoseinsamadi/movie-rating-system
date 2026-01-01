from pydantic import BaseModel
from typing import Optional


class GenreResponse(BaseModel):
    """پاسخ ژانر"""
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class GenreDetailResponse(GenreResponse):
    """پاسخ جزئی ژانر"""
    movies_count: int = 0
