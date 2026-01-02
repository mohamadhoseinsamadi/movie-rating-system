from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.models.rating import MovieRating
from app.repositories.movie_repository import MovieRepository
from app.repositories.genre_repository import GenreRepository
from app.repositories.director_repository import DirectorRepository
from app.exceptions.custom_exceptions import (
    NotFoundError,
    ValidationError
)


class MovieService:
    """Movie management service"""

    def __init__(self, db: Session):
        """Initialize with repositories"""
        self.movie_repo = MovieRepository(db)
        self.genre_repo = GenreRepository(db)
        self.director_repo = DirectorRepository(db)
        self.db = db

    def get_all_movies(
            self,
            page: int = 1,
            page_size: int = 10,
            title: Optional[str] = None,
            release_year: Optional[int] = None,
            genre: Optional[str] = None
    ) -> Tuple[List[Movie], int]:
        """
        Get all movies with filtering and pagination
        """
        if page < 1:
            raise ValidationError(f"Page must be positive, received: {page}")

        skip = (page - 1) * page_size

        movies = self.movie_repo.search_movies(
            skip=skip,
            limit=page_size,
            title=title,
            release_year=release_year,
            genre_name=genre
        )

        total_items = self.movie_repo.count_with_filters(
            title=title,
            release_year=release_year,
            genre_name=genre
        )

        return movies, total_items

    def get_movie_by_id(self, movie_id: int) -> Movie:
        """Get movie by ID"""
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise NotFoundError(f"Movie with ID {movie_id} not found")
        return movie

    def _validate_director(self, director_id: int):
        """Helper to validate director existence and ID limits"""
        if director_id > 2147483647:
            raise ValidationError(f"Invalid director_id: {director_id} (ID too large)")

        director = self.director_repo.get_by_id(director_id)
        if not director:
            raise ValidationError(f"Director with id {director_id} not found")
        return director

    def create_movie(self, title: str, director_id: int, release_year: int,
                     cast: str, genres: Optional[List[int]] = None) -> Movie:
        """Create a new movie"""
        if not title or len(title.strip()) == 0:
            raise ValidationError("Movie title cannot be empty")

        self._validate_director(director_id)

        valid_genres = []
        if genres:
            for genre_id in genres:
                if genre_id > 2147483647:
                    raise ValidationError(f"Invalid genre_id: {genre_id}")

                genre = self.genre_repo.get_by_id(genre_id)
                if not genre:
                    raise ValidationError(f"Genre with id {genre_id} not found")
                valid_genres.append(genre)

        movie = self.movie_repo.create(
            title=title,
            director_id=director_id,
            release_year=release_year,
            cast=cast
        )

        if valid_genres:
            movie.genres.extend(valid_genres)
            self.db.commit()

        return movie

    def update_movie(self, movie_id: int, title: Optional[str] = None,
                     director_id: Optional[int] = None, release_year: Optional[int] = None,
                     cast: Optional[str] = None, genres: Optional[List[int]] = None) -> Movie:
        """Update a movie"""
        movie = self.get_movie_by_id(movie_id)

        if title is not None:
            if not title.strip():
                raise ValidationError("Movie title cannot be empty")
            movie.title = title

        if director_id is not None:
            self._validate_director(director_id)
            movie.director_id = director_id

        if release_year is not None: movie.release_year = release_year
        if cast is not None: movie.cast = cast

        if genres is not None:
            new_genres = []
            for genre_id in genres:
                if genre_id > 2147483647:
                    raise ValidationError(f"Invalid genre_id: {genre_id}")

                genre = self.genre_repo.get_by_id(genre_id)
                if not genre:
                    raise ValidationError(f"Genre with id {genre_id} not found")
                new_genres.append(genre)

            movie.genres = new_genres

        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete_movie(self, movie_id: int) -> None:
        """Delete a movie by ID"""
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise NotFoundError(f"Movie with ID {movie_id} not found")

        self.movie_repo.delete_ratings_by_movie_id(movie_id)
        self.movie_repo.delete(movie_id)

    def add_rating(self, movie_id: int, score: int) -> MovieRating:
        """Add a rating to a movie"""
        self.get_movie_by_id(movie_id)

        if not (1 <= score <= 10):
            raise ValidationError(
                f"Rating must be between 1 and 10, received: {score}"
            )

        rating = MovieRating(movie_id=movie_id, score=score)
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)

        return rating

    def get_movie_stats(self, movie_id: int) -> Dict:
        """Get movie statistics"""
        self.get_movie_by_id(movie_id)
        return self.movie_repo.get_movie_stats(movie_id)
