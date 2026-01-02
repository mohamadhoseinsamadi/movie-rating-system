from typing import Dict, Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.genre_service import GenreService
from app.schemas.request.genre_schema import GenreCreateRequest, GenreUpdateRequest

router = APIRouter(prefix="/api/v1/genres", tags=["genres"])


def success(data: Any) -> Dict[str, Any]:
    """Success response"""
    return {"status": "success", "data": data}


@router.get("", response_model=Dict[str, Any])
async def list_genres(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List genres with pagination"""
    service = GenreService(db)
    skip = (page - 1) * page_size

    genres = service.get_all_genres(skip=skip, limit=page_size)
    total = service.get_total_count()

    items = [
        {
            "id": g.id,
            "name": g.name,
            "description": g.description,
        }
        for g in genres
    ]

    return success({
        "page": page,
        "page_size": page_size,
        "total_items": total,
        "items": items,
    })


@router.get("/{genre_id}", response_model=Dict[str, Any])
async def get_genre(genre_id: int, db: Session = Depends(get_db)):
    """Genre details"""
    service = GenreService(db)
    genre = service.get_genre(genre_id)

    return success({
        "id": genre.id,
        "name": genre.name,
        "description": genre.description,
        "movies_count": len(genre.movies),
    })


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
async def create_genre(
    body: GenreCreateRequest,
    db: Session = Depends(get_db),
):
    """Add a new genre"""
    service = GenreService(db)
    genre = service.create_genre(
        name=body.name,
        description=body.description,
    )

    return success({
        "id": genre.id,
        "name": genre.name,
        "description": genre.description,
    })


@router.put("/{genre_id}", response_model=Dict[str, Any])
async def update_genre(
    genre_id: int,
    body: GenreUpdateRequest,
    db: Session = Depends(get_db),
):
    """Update a genre"""
    service = GenreService(db)
    genre = service.update_genre(
        genre_id=genre_id,
        name=body.name,
        description=body.description,
    )

    return success({
        "id": genre.id,
        "name": genre.name,
        "description": genre.description,
    })


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    """Delete a genre"""
    service = GenreService(db)
    service.delete_genre(genre_id)
    return None
