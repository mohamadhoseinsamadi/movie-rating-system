from pydantic import BaseModel, Field
from typing import Optional, List


class MovieCreateRequest(BaseModel):
    """Request to create a movie"""
    title: str = Field(..., min_length=1, max_length=255, description="Movie title")
    director_id: int = Field(..., gt=0, description="Director ID")
    release_year: int = Field(..., ge=1800, le=2100, description="Release year")
    cast: Optional[str] = Field(None, max_length=5000, description="Cast")
    genres: List[int] = Field(..., min_length=1, description="List of genre IDs")


class MovieUpdateRequest(BaseModel):
    """Request to update a movie"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    release_year: Optional[int] = Field(None, ge=1800, le=2100)
    cast: Optional[str] = Field(None, max_length=5000)
    genres: Optional[List[int]] = Field(None, min_length=1)
