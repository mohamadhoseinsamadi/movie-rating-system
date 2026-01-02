from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.base import Base


class Director(Base):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    birth_year = Column(Integer)
    description = Column(Text)

    # Relationships
    movies = relationship("Movie", back_populates="director", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Director(id={self.id}, name='{self.name}')>"
