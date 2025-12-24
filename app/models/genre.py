from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)

    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"
