import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

from app.db.database import engine
from app.models.base import Base
from app.controllers import director_router, genre_router, movie_router
from app.logging_config import setup_logging

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Rating System API",
    description="Backend API for movie management and rating system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

logger = logging.getLogger("main")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code >= 500:
        logger.error(f"Server Error: {exc.detail}", exc_info=True)
    else:
        logger.warning(f"HTTP Error {exc.status_code}: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "failure",
            "error": {
                "code": exc.status_code,
                "message": str(exc.detail)
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle input validation errors"""
    logger.warning(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "failure",
            "error": {
                "code": 422,
                "message": "Validation error",
                "details": exc.errors()
            }
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors (500)"""
    logger.error(f"Global exception: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "failure",
            "error": {
                "code": 500,
                "message": "Internal server error"
            }
        }
    )


@app.on_event("startup")
async def startup_event():
    logger.info("Movie management system started")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Movie management system stopped")


@app.get("/")
async def read_root():
    return {"message": "Welcome to Movie Rating System"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}


app.include_router(director_router)
app.include_router(genre_router)
app.include_router(movie_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
