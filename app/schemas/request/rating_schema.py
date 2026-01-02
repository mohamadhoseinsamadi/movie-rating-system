from pydantic import BaseModel, Field


class RatingCreateRequest(BaseModel):
    """Request to create a rating"""
    score: int = Field(..., ge=1, le=10, description="Rating from 1 to 10")
