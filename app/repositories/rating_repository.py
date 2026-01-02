from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.rating import Rating, MovieRating
from app.repositories.base_repository import BaseRepository


class RatingRepository(BaseRepository[Rating]):
    """Repository برای Rating"""

    def __init__(self, db: Session):
        super().__init__(db, Rating)

    def get_by_movie_id(self, movie_id: int):
        """گرفتن تمام امتیازهای یک فیلم"""
        return self.db.query(Rating).filter(Rating.movie_id == movie_id).all()

    def get_average_rating(self, movie_id: int) -> float:
        """میانگین امتیاز فیلم"""
        result = self.db.query(func.avg(Rating.score)).filter(
            Rating.movie_id == movie_id
        ).scalar()
        return round(result, 1) if result else None

    def get_ratings_count(self, movie_id: int) -> int:
        """تعداد امتیازات فیلم"""
        return self.db.query(func.count(Rating.id)).filter(
            Rating.movie_id == movie_id
        ).scalar()

