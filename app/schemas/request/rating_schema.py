from pydantic import BaseModel, Field


class RatingCreateRequest(BaseModel):
    """درخواست ایجاد امتیاز"""
    score: int = Field(..., ge=1, le=10, description="امتیاز از 1 تا 10")
