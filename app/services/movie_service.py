from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.movie import Movie
from app.models.genre import Genre
from app.models.rating import MovieRating
from app.repositories.movie_repository import MovieRepository
from app.exceptions.custom_exceptions import (
    NotFoundError,
    ValidationError
)


class MovieService:
    """سرویس مدیریت فیلم‌ها"""

    def __init__(self, db: Session):
        """مقدار دهی اولیه"""
        self.movie_repo = MovieRepository(db)
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
        دریافت تمام فیلم‌ها با فیلتر و صفحه‌بندی

        Args:
            page: شماره صفحه
            page_size: تعداد آیتم در هر صفحه
            title: فیلتر بر اساس عنوان
            release_year: فیلتر بر اساس سال
            genre: فیلتر بر اساس ژانر

        Returns:
            (لیست فیلم‌ها، تعداد کل)
        """
        # Validate page
        if page < 1:
            raise ValidationError(f"صفحه باید مثبت باشد، دریافت شده: {page}")

        # Get base query
        query = self.db.query(Movie)

        # Apply filters
        if title:
            # جست‌وجو بر اساس عنوان (Case-insensitive)
            query = query.filter(Movie.title.ilike(f"%{title}%"))

        if release_year:
            # فیلتر بر اساس سال (دقیق)
            query = query.filter(Movie.release_year == release_year)

        if genre:
            # فیلتر بر اساس ژانر
            query = query.join(Movie.genres).filter(
                Genre.name.ilike(f"%{genre}%")
            ).distinct()

        # Get total count before pagination
        total_items = query.count()

        # Apply pagination
        skip = (page - 1) * page_size
        movies = query.offset(skip).limit(page_size).all()

        return movies, total_items

    def get_movie_by_id(self, movie_id: int) -> Movie:
        """
        دریافت فیلم بر اساس ID

        Args:
            movie_id: شناسه فیلم

        Returns:
            Movie object

        Raises:
            NotFoundError: اگر فیلم یافت نشود
        """
        movie = self.movie_repo.get_by_id(movie_id)

        if not movie:
            raise NotFoundError(f"فیلم با ID {movie_id} یافت نشد")

        return movie

    def create_movie(self, title: str, director_id: int, release_year: int,
                     cast: str, genres: Optional[List[int]] = None) -> Movie:
        """
        ایجاد فیلم جدید

        Args:
            title: عنوان فیلم
            director_id: شناسه کارگردان
            release_year: سال انتشار
            cast: بازیگران
            genres: لیست IDs ژانر

        Returns:
            Movie object

        Raises:
            ValidationError: اگر عنوان خالی باشد
        """
        # Validate
        if not title or len(title.strip()) == 0:
            raise ValidationError("عنوان فیلم نمی‌تواند خالی باشد")

        # Create movie
        movie = self.movie_repo.create(
            title=title,
            director_id=director_id,
            release_year=release_year,
            cast=cast
        )

        # Add genres if provided
        if genres:
            for genre_id in genres:
                genre = self.db.query(Genre).filter(Genre.id == genre_id).first()
                if genre:
                    movie.genres.append(genre)

        self.db.commit()
        return movie

