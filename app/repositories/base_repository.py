from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.base import Base
from app.exceptions.custom_exceptions import NotFoundError

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    """Base class for all repositories"""

    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, **kwargs) -> T:
        """Create a new record"""
        obj = self.model(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_by_id(self, id: int) -> Optional[T]:
        """Get record by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 10) -> List[T]:
        """Get all records with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def count(self) -> int:
        """Total number of records"""
        return self.db.query(func.count(self.model.id)).scalar()

    def update(self, id: int, **kwargs) -> T:
        """Update a record"""
        obj = self.get_by_id(id)
        if not obj:
            raise NotFoundError(f"{self.model.__name__} not found")

        for key, value in kwargs.items():
            if value is not None:
                setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        """Delete a record"""
        obj = self.get_by_id(id)
        if not obj:
            raise NotFoundError(f"{self.model.__name__} not found")

        self.db.delete(obj)
        self.db.commit()
        return True

    def delete_all(self):
        """Delete all records (for testing)"""
        self.db.query(self.model).delete()
        self.db.commit()
