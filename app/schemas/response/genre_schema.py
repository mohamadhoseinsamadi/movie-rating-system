from pydantic import BaseModel
from typing import Optional


class GenreResponse(BaseModel):
    """Genre Response"""
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class GenreDetailResponse(GenreResponse):
    """Genre Response in details"""
    movies_count: int = 0
