from typing import List, Dict
from sqlalchemy.orm import Session

from app.models.rating import Rating
from app.repositories.rating_repository import RatingRepository
from app.exceptions.custom_exceptions import NotFoundError, ValidationError


class RatingService:
    """سرویس مدیریت امتیازها"""

    def __init__(self, db: Session):
        """مقدار دهی اولیه"""
        self.rating_repo = RatingRepository(db)
        self.db = db

    def create_rating(self, movie_id: int, score: int) -> Rating:
        """
        ایجاد امتیاز جدید برای فیلم

        Args:
            movie_id: شناسه فیلم
            score: امتیاز (1 تا 10)

        Returns:
            Rating object

        Raises:
            ValidationError: اگر امتیاز معتبر نباشد
        """
        # Validate score
        if score < 1 or score > 10:
            raise ValidationError("امتیاز باید بین 1 تا 10 باشد")

        # Create rating
        rating = self.rating_repo.create(
            movie_id=movie_id,
            score=score
        )

        return rating

    def get_movie_ratings(self, movie_id: int) -> List[Rating]:
        """
        دریافت تمام امتیازهای یک فیلم

        Args:
            movie_id: شناسه فیلم

        Returns:
            List of Rating objects
        """
        return self.rating_repo.get_by_movie_id(movie_id)

    def get_movie_rating_stats(self, movie_id: int) -> Dict:
        """
        دریافت آمار امتیازهای یک فیلم

        Args:
            movie_id: شناسه فیلم

        Returns:
            Dict شامل average_rating و ratings_count
        """
        average_rating = self.rating_repo.get_average_rating(movie_id)
        ratings_count = self.rating_repo.get_ratings_count(movie_id)

        return {
            "average_rating": round(average_rating, 1) if average_rating else None,
            "ratings_count": ratings_count or 0
        }



