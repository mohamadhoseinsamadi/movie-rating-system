from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status, Body
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.movie_service import MovieService
from app.services.rating_service import RatingService
from app.schemas.request.movie_schema import MovieCreateRequest, MovieUpdateRequest
from app.schemas.request.rating_schema import RatingCreateRequest
from app.exceptions.custom_exceptions import NotFoundError, ValidationError

router = APIRouter(prefix="/api/v1", tags=["movies"])


@router.get("/movies", response_model=dict)
async def get_movies(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        title: Optional[str] = Query(None),
        release_year: Optional[int] = Query(None),
        genre: Optional[str] = Query(None),
        db: Session = Depends(get_db)
):
    """
    Get list of movies with filtering and pagination

    Query Parameters:
    - page: Page number (default: 1)
    - page_size: Items per page (default: 10, maximum: 100)
    - title: Search by title
    - release_year: Filter by release year (example: 2008)
    - genre: Filter by genre
    """
    try:
        service = MovieService(db)

        movies, total_items = service.get_all_movies(
            page=page,
            page_size=page_size,
            title=title,
            release_year=release_year,
            genre=genre
        )

        items = []
        for movie in movies:
            item = {
                "id": movie.id,
                "title": movie.title,
                "release_year": movie.release_year,
                "director": {
                    "id": movie.director.id,
                    "name": movie.director.name
                } if movie.director else None,
                "genres": [genre.name for genre in movie.genres],
                "cast": movie.cast,
                "average_rating": None,
                "ratings_count": 0
            }

            stats = service.get_movie_stats(movie.id)
            item["average_rating"] = stats["average_rating"]
            item["ratings_count"] = stats["ratings_count"]

            items.append(item)

        return {
            "status": "success",
            "data": {
                "page": page,
                "page_size": page_size,
                "total_items": total_items,
                "items": items
            }
        }

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {str(e)}"
        )


@router.get("/movies/{movie_id}", response_model=dict)
async def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Get details of a specific movie"""
    try:
        service = MovieService(db)
        movie = service.get_movie_by_id(movie_id)

        stats = service.get_movie_stats(movie_id)

        return {
            "status": "success",
            "data": {
                "id": movie.id,
                "title": movie.title,
                "release_year": movie.release_year,
                "director": {
                    "id": movie.director.id,
                    "name": movie.director.name
                } if movie.director else None,
                "genres": [genre.name for genre in movie.genres],
                "cast": movie.cast,
                "average_rating": stats["average_rating"],
                "ratings_count": stats["ratings_count"]
            }
        }

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.post("/movies", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_movie(
        movie_data: MovieCreateRequest = Body(...),
        db: Session = Depends(get_db)
):
    """Create a new movie"""
    try:
        service = MovieService(db)

        movie = service.create_movie(
            title=movie_data.title,
            director_id=movie_data.director_id,
            release_year=movie_data.release_year,
            cast=movie_data.cast,
            genres=movie_data.genres
        )

        stats = service.get_movie_stats(movie.id)

        return {
            "status": "success",
            "data": {
                "id": movie.id,
                "title": movie.title,
                "release_year": movie.release_year,
                "director_id": movie.director_id,
                "cast": movie.cast,
                "genres": [g.name for g in movie.genres],
                "average_rating": stats["average_rating"],
                "ratings_count": stats["ratings_count"]
            }
        }

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.put("/movies/{movie_id}", response_model=dict)
async def update_movie(
        movie_id: int,
        movie_data: MovieUpdateRequest = Body(...),
        db: Session = Depends(get_db)
):
    """Update a movie"""
    try:
        service = MovieService(db)

        movie = service.update_movie(
            movie_id=movie_id,
            title=movie_data.title,
            director_id=movie_data.director_id if hasattr(movie_data, 'director_id') else None,
            release_year=movie_data.release_year,
            cast=movie_data.cast,
            genres=movie_data.genres
        )

        stats = service.get_movie_stats(movie.id)

        return {
            "status": "success",
            "data": {
                "id": movie.id,
                "title": movie.title,
                "release_year": movie.release_year,
                "cast": movie.cast,
                "genres": [g.name for g in movie.genres],
                "average_rating": stats["average_rating"],
                "ratings_count": stats["ratings_count"]
            }
        }

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """Delete a movie"""
    try:
        service = MovieService(db)
        service.delete_movie(movie_id)
        return None

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.post("/movies/{movie_id}/ratings", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_rating(
    movie_id: int,
    rating_data: RatingCreateRequest = Body(...),
    db: Session = Depends(get_db)
):
    """Create a new rating for a movie"""
    try:
        # Check if movie exists
        movie_service = MovieService(db)
        movie_service.get_movie_by_id(movie_id)

        # Create rating
        rating_service = RatingService(db)
        rating = rating_service.create_rating(
            movie_id=movie_id,
            score=rating_data.score
        )

        return {
            "status": "success",
            "data": {
                "id": rating.id,
                "movie_id": rating.movie_id,
                "score": rating.score,
                "created_at": rating.created_at.isoformat() if rating.created_at else None
            }
        }

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.get("/movies/{movie_id}/ratings", response_model=dict)
async def get_movie_ratings(movie_id: int, db: Session = Depends(get_db)):
    """Get all ratings for a movie with statistics"""
    try:
        # Check if movie exists
        movie_service = MovieService(db)
        movie_service.get_movie_by_id(movie_id)

        # Get ratings and stats
        rating_service = RatingService(db)
        ratings = rating_service.get_movie_ratings(movie_id)
        stats = rating_service.get_movie_rating_stats(movie_id)

        return {
            "status": "success",
            "data": {
                "movie_id": movie_id,
                "average_rating": stats["average_rating"],
                "ratings_count": stats["ratings_count"],
                "ratings": [
                    {
                        "id": rating.id,
                        "score": rating.score,
                        "created_at": rating.created_at.isoformat() if rating.created_at else None
                    }
                    for rating in ratings
                ]
            }
        }

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )
