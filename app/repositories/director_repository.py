from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.director import Director
from app.repositories.base_repository import BaseRepository


class DirectorRepository(BaseRepository[Director]):
    """Repository for Director"""

    def __init__(self, db: Session):
        super().__init__(db, Director)

    def get_by_name(self, name: str) -> Director:
        """Search by name"""
        return self.db.query(Director).filter(Director.name == name).first()

    def get_directors_with_movies(self, skip: int = 0, limit: int = 10):
        """Get directors with their movie count"""
        return self.db.query(Director).offset(skip).limit(limit).all()
