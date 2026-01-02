from sqlalchemy.orm import Session
from app.repositories.director_repository import DirectorRepository
from app.exceptions.custom_exceptions import NotFoundError, ValidationError


class DirectorService:
    """Business logic for directors"""

    def __init__(self, db: Session):
        self.repo = DirectorRepository(db)

    def get_all_directors(self, skip: int = 0, limit: int = 10):
        """List directors"""
        return self.repo.get_all(skip, limit)

    def get_total_count(self) -> int:
        """Total number of directors"""
        return self.repo.count()

    def get_director(self, director_id: int):
        """Get director details"""
        director = self.repo.get_by_id(director_id)
        if not director:
            raise NotFoundError(f"Director with id {director_id} not found")
        return director

    def create_director(self, name: str, birth_year: int = None,
                        description: str = None):
        """Create a new director"""
        # Validation
        if not name or len(name.strip()) == 0:
            raise ValidationError("Director name cannot be empty")

        if len(name) > 255:
            raise ValidationError("Director name must be less than 255 characters")

        if birth_year and (birth_year < 1800 or birth_year > 2100):
            raise ValidationError("Birth year must be between 1800 and 2100")

        return self.repo.create(
            name=name.strip(),
            birth_year=birth_year,
            description=description
        )

    def update_director(self, director_id: int, name: str = None,
                        birth_year: int = None, description: str = None):
        """Update a director"""
        # Check exists
        director = self.repo.get_by_id(director_id)
        if not director:
            raise NotFoundError(f"Director with id {director_id} not found")

        # Validation
        if name and len(name.strip()) == 0:
            raise ValidationError("Director name cannot be empty")

        if name and len(name) > 255:
            raise ValidationError("Director name must be less than 255 characters")

        if birth_year and (birth_year < 1800 or birth_year > 2100):
            raise ValidationError("Birth year must be between 1800 and 2100")

        return self.repo.update(
            director_id,
            name=name.strip() if name else None,
            birth_year=birth_year,
            description=description
        )

    def delete_director(self, director_id: int):
        """Delete director and all associated movies"""
        director = self.repo.get_by_id(director_id)
        if not director:
            raise NotFoundError(f"Director with id {director_id} not found")

        return self.repo.delete(director_id)
