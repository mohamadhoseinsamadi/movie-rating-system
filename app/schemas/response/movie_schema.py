from pydantic import BaseModel
from typing import Optional, List


class DirectorMinimal(BaseModel):
    """کارگردان خلاصه"""
    id: int
    name: str


class GenreMinimal(BaseModel):
    """ژانر خلاصه"""
    id: int
    name: str


class MovieResponse(BaseModel):
    """پاسخ فیلم"""
    id: int
    title: str
    release_year: int
    director: DirectorMinimal
    genres: List[str]
    average_rating: Optional[float] = None
    ratings_count: int = 0

    class Config:
        from_attributes = True


class MovieDetailResponse(MovieResponse):
    """پاسخ جزئی فیلم"""
    cast: Optional[str] = None
    director: Optional[dict] = None  # کارگردان کامل


class MoviePaginatedResponse(BaseModel):
    """لیست صفحه‌بندی شده‌ی فیلم‌ها"""
    page: int
    page_size: int
    total_items: int
    items: List[MovieResponse]
