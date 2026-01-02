from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import Base

# Association table for many-to-many relationship between Movie and Genre
movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    director_id = Column(Integer, ForeignKey('directors.id'), nullable=False)
    release_year = Column(Integer)
    cast = Column(Text)

    # Relationships
    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Movie(id={self.id}, title=\"{self.title}\")>'
