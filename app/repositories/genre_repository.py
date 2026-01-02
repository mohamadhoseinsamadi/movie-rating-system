from sqlalchemy.orm import Session
from app.models.genre import Genre
from app.repositories.base_repository import BaseRepository


class GenreRepository(BaseRepository[Genre]):
    """Repository for Genre"""

    def __init__(self, db: Session):
        super().__init__(db, Genre)

    def get_by_name(self, name: str) -> Genre:
        """Search by name"""
        return self.db.query(Genre).filter(Genre.name == name).first()

    def get_genres_with_movies(self, skip: int = 0, limit: int = 10):
        """Get genres with their movie count"""
        return self.db.query(Genre).offset(skip).limit(limit).all()
