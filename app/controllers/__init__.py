from app.controllers.director_controller import router as director_router
from app.controllers.genre_controller import router as genre_router
from app.controllers.movie_controller import router as movie_router

__all__ = [
    "director_router",
    "genre_router",
    "movie_router"
]
