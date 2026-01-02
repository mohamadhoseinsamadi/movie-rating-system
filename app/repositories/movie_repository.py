from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie import movie_genres
from app.models.rating import MovieRating
from app.repositories.base_repository import BaseRepository


class MovieRepository(BaseRepository[Movie]):
    """Repository for Movie - includes filtering and pagination"""

    def __init__(self, db: Session):
        super().__init__(db, Movie)

    def search_movies(
            self,
            skip: int = 0,
            limit: int = 10,
            title: Optional[str] = None,
            release_year: Optional[int] = None,
            genre_name: Optional[str] = None
    ) -> List[Movie]:
        """
        Search movies with combined filters and pagination.
        Handles joins properly for genre filtering.
        """
        query = self.db.query(Movie)

        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))

        if release_year:
            query = query.filter(Movie.release_year == release_year)

        if genre_name:
            query = query.join(Movie.genres).filter(
                Genre.name.ilike(f"%{genre_name}%")
            )

        query = query.distinct()

        return query.offset(skip).limit(limit).all()

    def count_with_filters(
            self,
            title: Optional[str] = None,
            release_year: Optional[int] = None,
            genre_name: Optional[str] = None
    ) -> int:
        """Count movies matching the filters"""
        query = self.db.query(func.count(Movie.id))

        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))

        if release_year:
            query = query.filter(Movie.release_year == release_year)

        if genre_name:
            query = query.join(Movie.genres).filter(
                Genre.name.ilike(f"%{genre_name}%")
            )

        return query.scalar()

    def get_movie_stats(self, movie_id: int) -> Dict[str, float]:
        """
        Get aggregated statistics for a movie (avg rating, count).
        Moved from Service to Repository (Data Access Layer).
        """
        stats = self.db.query(
            func.avg(MovieRating.score).label("average_rating"),
            func.count(MovieRating.id).label("ratings_count")
        ).filter(MovieRating.movie_id == movie_id).first()

        return {
            "average_rating": float(stats.average_rating) if stats.average_rating else None,
            "ratings_count": stats.ratings_count or 0
        }

    def delete_ratings_by_movie_id(self, movie_id: int):
        """Delete all ratings for a specific movie"""
        self.db.query(MovieRating).filter(MovieRating.movie_id == movie_id).delete()
        self.db.commit()
