from sqlalchemy.orm import Session
from app.models.genre import Genre  # یا app.models import Genre
from app.repositories.genre_repository import GenreRepository
from app.exceptions.custom_exceptions import NotFoundError


class GenreService:
    """سرویس مدیریت ژانرها - حداقل پیاده‌سازی برای رفع خطا"""

    def __init__(self, db: Session):
        self.repo = GenreRepository(db)

    def get_all_genres(self, skip: int = 0, limit: int = 100):
        """دریافت لیست ژانرها"""
        return self.repo.get_all(skip=skip, limit=limit)

    def get_genre_by_id(self, genre_id: int):
        """دریافت یک ژانر بر اساس ID"""
        genre = self.repo.get_by_id(genre_id)
        if not genre:
            raise NotFoundError(f"Genre with id {genre_id} not found")
        return genre

    def get_genre_by_name(self, name: str):
        """دریافت ژانر بر اساس نام (برای فیلتر فیلم)"""
        return self.repo.get_by_name(name)