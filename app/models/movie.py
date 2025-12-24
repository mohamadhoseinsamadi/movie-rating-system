from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    director_id = Column(Integer, ForeignKey('directors.id'), nullable=False)
    release_year = Column(Integer)
    cast = Column(Text)

    def __repr__(self):
        return f'<Movie(id={self.id}, title=\"{self.title}\")>'
