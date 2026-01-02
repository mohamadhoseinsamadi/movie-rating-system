from pydantic import BaseModel, Field
from typing import Optional


class DirectorCreateRequest(BaseModel):
    """Request to create a director"""
    name: str = Field(..., min_length=1, max_length=255, description="Director's name")
    birth_year: Optional[int] = Field(None, ge=1800, le=2100, description="Birth year")
    description: Optional[str] = Field(None, max_length=5000, description="Description")


class DirectorUpdateRequest(BaseModel):
    """Request to update a director"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    birth_year: Optional[int] = Field(None, ge=1800, le=2100)
    description: Optional[str] = Field(None, max_length=5000)
