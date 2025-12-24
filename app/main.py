from fastapi import FastAPI
from app.db.database import engine
from app.models.base import Base
import uvicorn

app = FastAPI(
    title="Movie Rating System API",
    description="Backend API for movie management and rating system",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """
    Create tables when launching the application.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    print(f"Database URL: {engine.url}")


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Movie Rating System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected" if engine else "disconnected"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
