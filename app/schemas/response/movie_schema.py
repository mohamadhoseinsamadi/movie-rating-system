from pydantic import BaseModel
from typing import Optional, List


class DirectorMinimal(BaseModel):
    """Minimal director information"""
    id: int
    name: str


class GenreMinimal(BaseModel):
    """Minimal genre information"""
    id: int
    name: str


class MovieResponse(BaseModel):
    """Movie response"""
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
    """Detailed movie response"""
    cast: Optional[str] = None
    director: Optional[dict] = None


class MoviePaginatedResponse(BaseModel):
    """Paginated list of movies"""
    page: int
    page_size: int
    total_items: int
    items: List[MovieResponse]
