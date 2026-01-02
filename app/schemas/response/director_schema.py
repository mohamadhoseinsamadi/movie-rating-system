from pydantic import BaseModel
from typing import Optional


class DirectorResponse(BaseModel):
    """Director response"""
    id: int
    name: str
    birth_year: Optional[int] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class DirectorDetailResponse(DirectorResponse):
    """Detailed director response"""
    movies_count: int = 0
