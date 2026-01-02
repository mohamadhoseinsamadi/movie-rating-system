from sqlalchemy.orm import Session
from app.repositories.rating_repository import RatingRepository
from app.repositories.movie_repository import MovieRepository
from app.exceptions.custom_exceptions import NotFoundError, ValidationError


class RatingService:
    """Business logic for ratings"""

    def __init__(self, db: Session):
        self.repo = RatingRepository(db)
        self.movie_repo = MovieRepository(db)

    def create_rating(self, movie_id: int, score: int):
        """Create a new rating"""
        # Check movie exists
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise NotFoundError(f"Movie with id {movie_id} not found")

        # Validation score
        if not isinstance(score, int) or score < 1 or score > 10:
            raise ValidationError("Score must be an integer between 1 and 10")

        return self.repo.create(
            movie_id=movie_id,
            score=score
        )

    def get_movie_ratings(self, movie_id: int):
        """All ratings for a movie"""
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise NotFoundError(f"Movie with id {movie_id} not found")

        return self.repo.get_by_movie(movie_id)

    def get_average_rating(self, movie_id: int):
        """Average rating of a movie"""
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise NotFoundError(f"Movie with id {movie_id} not found")

        return self.repo.get_average(movie_id)

    def get_ratings_count(self, movie_id: int):
        """Number of ratings for a movie"""
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise NotFoundError(f"Movie with id {movie_id} not found")

        return self.repo.count_by_movie(movie_id)
