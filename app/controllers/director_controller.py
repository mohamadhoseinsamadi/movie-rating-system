from typing import Dict, Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.director_service import DirectorService
from app.schemas.request.director_schema import DirectorCreateRequest, DirectorUpdateRequest
from app.exceptions.custom_exceptions import NotFoundError

router = APIRouter(prefix="/api/v1/directors", tags=["directors"])


def success(data: Any) -> Dict[str, Any]:
    """Success response"""
    return {"status": "success", "data": data}


@router.get("", response_model=Dict[str, Any])
async def list_directors(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List directors with pagination"""
    service = DirectorService(db)
    skip = (page - 1) * page_size

    directors = service.get_all_directors(skip=skip, limit=page_size)
    total = service.get_total_count()

    items = [
        {
            "id": d.id,
            "name": d.name,
            "birth_year": d.birth_year,
            "description": d.description,
        }
        for d in directors
    ]

    return success({
        "page": page,
        "page_size": page_size,
        "total_items": total,
        "items": items,
    })


@router.get("/{director_id}", response_model=Dict[str, Any])
async def get_director(director_id: int, db: Session = Depends(get_db)):
    """Director details"""
    service = DirectorService(db)
    director = service.get_director(director_id)

    return success({
        "id": director.id,
        "name": director.name,
        "birth_year": director.birth_year,
        "description": director.description,
        "movies_count": len(director.movies),
    })


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
async def create_director(
    body: DirectorCreateRequest,
    db: Session = Depends(get_db),
):
    """Add a new director"""
    service = DirectorService(db)
    director = service.create_director(
        name=body.name,
        birth_year=body.birth_year,
        description=body.description,
    )

    return success({
        "id": director.id,
        "name": director.name,
        "birth_year": director.birth_year,
        "description": director.description,
    })


@router.put("/{director_id}", response_model=Dict[str, Any])
async def update_director(
    director_id: int,
    body: DirectorUpdateRequest,
    db: Session = Depends(get_db),
):
    """Update a director"""
    service = DirectorService(db)
    director = service.update_director(
        director_id=director_id,
        name=body.name,
        birth_year=body.birth_year,
        description=body.description,
    )

    return success({
        "id": director.id,
        "name": director.name,
        "birth_year": director.birth_year,
        "description": director.description,
        "updated_at": director.updated_at.isoformat() if director.updated_at else None,
    })


@router.delete("/{director_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_director(director_id: int, db: Session = Depends(get_db)):
    """Delete a director and all their movies"""
    service = DirectorService(db)
    service.delete_director(director_id)
    return None
