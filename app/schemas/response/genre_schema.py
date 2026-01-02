from pydantic import BaseModel
from typing import Optional


class GenreResponse(BaseModel):
    """Genre response"""
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class GenreDetailResponse(GenreResponse):
    """Detailed genre response"""
    movies_count: int = 0
