from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.director import Director
from app.repositories.base_repository import BaseRepository


class DirectorRepository(BaseRepository[Director]):
    """Repository برای Director"""

    def __init__(self, db: Session):
        super().__init__(db, Director)

    def get_by_name(self, name: str) -> Director:
        """جستجو بر اساس نام"""
        return self.db.query(Director).filter(Director.name == name).first()

    def get_directors_with_movies(self, skip: int = 0, limit: int = 10):
        """گرفتن کارگردان‌ها همراه با تعداد فیلم‌های آن‌ها"""
        return self.db.query(Director).offset(skip).limit(limit).all()
