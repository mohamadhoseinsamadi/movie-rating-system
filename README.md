# Movie Rating System API

A layered RESTful API for managing movies, directors, genres, and user ratings, built with **FastAPI** and **PostgreSQL**. The codebase follows a clean separation of concerns (controllers → services → repositories) with structured logging and standardized error responses.

## Features

- **Movie Management:** Create, update, delete, and retrieve movies.
- **Advanced Search & Filtering:** Filter movies by title, release year, and genre with pagination.
- **Director & Genre Management:** Manage metadata for movies.
- **Rating System:** Users can rate movies (1–10); average rating and rating count are computed automatically.
- **Data Consistency:** Cascade deletions ensure no orphaned data (e.g., deleting a movie deletes its ratings).
- **ETL Seeding:** Script to load real-world data from the TMDB 5000 dataset.
- **Structured Logging:** Configurable logging (INFO, WARNING, ERROR) for monitoring.
- **Standardized Responses:** Unified JSON structure for both success and error responses.

## Tech Stack

- **Language:** Python 3.9+
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (migrations in `alembic/`)
- **Validation:** Pydantic
- **Server:** Uvicorn
- **Containerization:** Docker + docker-compose

## Quickstart (Docker)

```bash
docker compose up --build
```

This starts PostgreSQL and the API. Once running:

- API root: http://localhost:8000
- Interactive docs (Swagger UI): http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Local Development

1. Copy `.env.example` to `.env` and set `DATABASE_URL` to your PostgreSQL instance.
2. Install dependencies:

   ```bash
   poetry install
   ```

3. Run the server:

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

Database tables are created automatically at startup.

## Database Seeding (ETL)

The dataset files are **not included** in this repository (they are ~45 MB).

1. Download `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` from [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
2. Place the CSV files inside the `scripts/` folder.
3. Run the seeder:

   ```bash
   python scripts/seed.py
   ```

## Project Structure

```
app/
  controllers/    # HTTP layer (routers, request handling)
  services/       # Business logic
  repositories/   # Data access
  models/         # SQLAlchemy ORM models
  schemas/        # Pydantic request/response schemas
  db/             # Engine and session setup
  exceptions/     # Custom exception types
alembic/          # Database migrations
scripts/          # ETL seeding scripts
```

## License

MIT — see [LICENSE](LICENSE).