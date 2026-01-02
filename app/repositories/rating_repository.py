from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.rating import MovieRating
from app.repositories.base_repository import BaseRepository


class RatingRepository(BaseRepository[MovieRating]):
    """Repository for MovieRating"""

    def __init__(self, db: Session):
        super().__init__(db, MovieRating)

    def get_by_movie(self, movie_id: int):
        """Get all ratings for a movie"""
        return self.db.query(MovieRating).filter(
            MovieRating.movie_id == movie_id
        ).all()

    def get_average(self, movie_id: int) -> float:
        """Average rating of a movie"""
        result = self.db.query(func.avg(MovieRating.score)).filter(
            MovieRating.movie_id == movie_id
        ).scalar()
        return round(result, 1) if result else None

    def count_by_movie(self, movie_id: int) -> int:
        """Number of ratings for a movie"""
        return self.db.query(func.count(MovieRating.id)).filter(
            MovieRating.movie_id == movie_id
        ).scalar()
