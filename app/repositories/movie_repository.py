from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.movie import Movie
from app.models.rating import MovieRating
from app.repositories.base_repository import BaseRepository


class MovieRepository(BaseRepository[Movie]):
    """Repository برای Movie - شامل filtering و pagination"""

    def __init__(self, db: Session):
        super().__init__(db, Movie)

    def get_paginated(self, skip: int = 0, limit: int = 10):
        """صفحه‌بندی فیلم‌ها"""
        return self.db.query(Movie).offset(skip).limit(limit).all()

    def filter_by_title(self, title: str, skip: int = 0, limit: int = 10):
        """جستجو بر اساس عنوان (بخشی)"""
        query = self.db.query(Movie).filter(
            Movie.title.ilike(f"%{title}%")
        )
        return query.offset(skip).limit(limit).all()

    def filter_by_year(self, year: int, skip: int = 0, limit: int = 10):
        """جستجو بر اساس سال انتشار"""
        return self.db.query(Movie).filter(
            Movie.release_year == year
        ).offset(skip).limit(limit).all()

    def filter_by_genre(self, genre_id: int, skip: int = 0, limit: int = 10):
        """جستجو بر اساس ژانر"""
        from app.models.movie import movie_genres
        return self.db.query(Movie).join(movie_genres).filter(
            movie_genres.c.genre_id == genre_id
        ).offset(skip).limit(limit).all()

    def filter_combined(self, title: str = None, year: int = None,
                        genre_id: int = None, skip: int = 0, limit: int = 10):
        """جستجو با ترکیب چند فیلتر"""
        query = self.db.query(Movie)

        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if year:
            query = query.filter(Movie.release_year == year)
        if genre_id:
            from app.models.movie import movie_genres
            query = query.join(movie_genres).filter(
                movie_genres.c.genre_id == genre_id
            )

        return query.offset(skip).limit(limit).all()

    def count_with_filters(self, title: str = None, year: int = None,
                           genre_id: int = None) -> int:
        """تعداد فیلم‌ها با فیلترها"""
        query = self.db.query(func.count(Movie.id))

        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if year:
            query = query.filter(Movie.release_year == year)
        if genre_id:
            from app.models.movie import movie_genres
            query = query.join(movie_genres).filter(
                movie_genres.c.genre_id == genre_id
            )

        return query.scalar()

    def get_average_rating(self, movie_id: int) -> float:
        """میانگین امتیاز فیلم"""
        result = self.db.query(func.avg(MovieRating.score)).filter(
            MovieRating.movie_id == movie_id
        ).scalar()
        return round(result, 1) if result else None

    def get_ratings_count(self, movie_id: int) -> int:
        """تعداد امتیازات فیلم"""
        return self.db.query(func.count(MovieRating.id)).filter(
            MovieRating.movie_id == movie_id
        ).scalar()

    def get_by_director(self, director_id: int, skip: int = 0, limit: int = 10):
        """گرفتن فیلم‌های یک کارگردان"""
        return self.db.query(Movie).filter(
            Movie.director_id == director_id
        ).offset(skip).limit(limit).all()