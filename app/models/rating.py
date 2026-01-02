from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Rating(Base):
    __tablename__ = 'movie_ratings'
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    score = Column(Integer, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    movie = relationship("Movie", back_populates="ratings")
    
    def __repr__(self):
        return f'<Rating(id={self.id}, movie_id={self.movie_id}, score={self.score})>'

# Alias for backward compatibility
MovieRating = Rating
