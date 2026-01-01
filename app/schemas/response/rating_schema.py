from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RatingResponse(BaseModel):
    """پاسخ امتیاز"""
    rating_id: int
    movie_id: int
    score: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
