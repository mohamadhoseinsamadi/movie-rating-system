from sqlalchemy.orm import Session
from app.repositories.genre_repository import GenreRepository
from app.exceptions.custom_exceptions import NotFoundError, ValidationError, ConflictError


class GenreService:
    """Business logic for genres"""

    def __init__(self, db: Session):
        self.repo = GenreRepository(db)

    def get_all_genres(self, skip: int = 0, limit: int = 10):
        """List genres"""
        return self.repo.get_all(skip, limit)

    def get_total_count(self) -> int:
        """Total number of genres"""
        return self.repo.count()

    def get_genre(self, genre_id: int):
        """Get genre details"""
        genre = self.repo.get_by_id(genre_id)
        if not genre:
            raise NotFoundError(f"Genre with id {genre_id} not found")
        return genre

    def create_genre(self, name: str, description: str = None):
        """Create a new genre"""
        if not name or len(name.strip()) == 0:
            raise ValidationError("Genre name cannot be empty")

        if len(name) > 100:
            raise ValidationError("Genre name must be less than 100 characters")

        existing = self.repo.get_by_name(name.strip())
        if existing:
            raise ConflictError(f"Genre with name '{name}' already exists")

        return self.repo.create(
            name=name.strip(),
            description=description
        )

    def update_genre(self, genre_id: int, name: str = None,
                     description: str = None):
        """Update a genre"""
        genre = self.repo.get_by_id(genre_id)
        if not genre:
            raise NotFoundError(f"Genre with id {genre_id} not found")

        if name and len(name.strip()) == 0:
            raise ValidationError("Genre name cannot be empty")

        if name and len(name) > 100:
            raise ValidationError("Genre name must be less than 100 characters")

        if name and name.strip() != genre.name:
            existing = self.repo.get_by_name(name.strip())
            if existing:
                raise ConflictError(f"Genre with name '{name}' already exists")

        return self.repo.update(
            genre_id,
            name=name.strip() if name else None,
            description=description
        )

    def delete_genre(self, genre_id: int):
        """Delete a genre (movies are not deleted)"""
        genre = self.repo.get_by_id(genre_id)
        if not genre:
            raise NotFoundError(f"Genre with id {genre_id} not found")

        return self.repo.delete(genre_id)
