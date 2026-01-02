from pydantic import BaseModel, Field
from typing import Optional


class GenreCreateRequest(BaseModel):
    """Request to create a genre"""
    name: str = Field(..., min_length=1, max_length=100, description="Genre name")
    description: Optional[str] = Field(None, max_length=5000, description="Description")


class GenreUpdateRequest(BaseModel):
    """Request to update a genre"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=5000)
