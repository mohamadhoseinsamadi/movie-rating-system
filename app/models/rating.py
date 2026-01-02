from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base


class MovieRating(Base):
    __tablename__ = "movie_ratings"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete='CASCADE'), nullable=False, index=True)
    score = Column(Integer, nullable=False)  # 1-10
    created_at = Column(DateTime, default=datetime.utcnow)

    movie = relationship("Movie", back_populates="ratings")

    def __repr__(self):
        return f"<MovieRating(id={self.id}, movie_id={self.movie_id}, score={self.score})>"
