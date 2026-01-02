from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base

movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True)
)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    director_id = Column(Integer, ForeignKey('directors.id', ondelete='CASCADE'), nullable=False)
    release_year = Column(Integer, nullable=False)
    cast = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    director = relationship("Director", back_populates="movies")
    genres = relationship(
        "Genre",
        secondary=movie_genres,
        back_populates="movies"
    )
    ratings = relationship("MovieRating", back_populates="movie", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}')>"

    def get_average_rating(self):
        """calculate average rating"""
        if not self.ratings:
            return None
        return sum(r.score for r in self.ratings) / len(self.ratings)

    def get_ratings_count(self):
        """ratings count"""
        return len(self.ratings)
