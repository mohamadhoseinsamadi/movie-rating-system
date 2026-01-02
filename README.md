# Movie Rating System

A backend system for managing movies and user ratings.

## Technologies
- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy
- Poetry

## Running the Application

**⚠️ IMPORTANT: You must run uvicorn from the ROOT directory, NOT from the scripts/ directory!**

To start the FastAPI server:

```bash
# First, make sure you're in the ROOT directory (where pyproject.toml is located)
# If you're in scripts/, go back:
cd ..

# Then run uvicorn:
poetry run uvicorn app.main:app --reload
```

Or using Python directly:

```bash
# From root directory:
python -m uvicorn app.main:app --reload
```

The API will be available at:
- API: http://127.0.0.1:8000
- Interactive Docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Database Seeding

This project includes a database seeding system that loads 1000 real movies from the TMDB 5000 dataset.

### Prerequisites

1. Ensure PostgreSQL is running and the database is created
2. Run Alembic migrations to create the schema:
   ```bash
   alembic upgrade head
   ```
3. Ensure the CSV files are in the `scripts/` directory:
   - `tmdb_5000_movies.csv`
   - `tmdb_5000_credits.csv`
   
   Download from: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

### Seeding the Database

To seed the database with 1000 movies from the TMDB 5000 dataset, simply run:

```bash
python scripts/seed.py
```

**What the seeding script does:**
- Cleans up existing data (drops and recreates tables)
- Loads CSV files from the `scripts/` directory
- Extracts and inserts genres (20 genres)
- Processes and inserts top 1000 movies by popularity
- Inserts directors (472+ directors)
- Generates random ratings (1-40 ratings per movie, scores 1-10)

**Expected output:**
```
============================================================
Starting Database Seeding (TMDB 5000 ETL)
============================================================

1. Cleaning up database...
   tables dropped and recreated.

2. Loading CSV data from scripts/tmdb_5000_movies.csv...

3. extracting Genres...
   Inserted 20 genres.

4. Processing Movies & Directors (Top 1000 by popularity)...
   Processed 1000 movies...
   Inserted 1000 movies and 472 directors.

5. Generating Random Ratings...
   Inserted 21000+ ratings.

============================================================
Seeding Completed Successfully!
============================================================
```

**Note:** 
- Make sure the CSV files (`tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`) are in the `scripts/` directory
- The script can be run from the root directory of the project
- Make sure PostgreSQL is running and the database is created before seeding

### Verification

After seeding, verify the data was loaded correctly:
```bash
python scripts/seed_check.py
```

Expected output:
- Movies loaded: 1000
- Directors loaded: 472+
- Genres loaded: 20
- Ratings generated: 21000+

## API Endpoints

The API uses pagination by default. To see all data, you can:

1. **Check if database is seeded:**
   ```bash
   python scripts/seed_check.py
   ```

2. **Use API with pagination:**
   - Movies: `GET /api/v1/movies?page=1&page_size=100`
   - Directors: `GET /api/v1/directors?page=1&page_size=100`
   - Genres: `GET /api/v1/genres?page=1&page_size=100`

3. **Available endpoints:**
   - `GET /api/v1/movies` - List movies (with pagination)
   - `GET /api/v1/movies/{id}` - Get movie details
   - `GET /api/v1/directors` - List directors (with pagination)
   - `GET /api/v1/directors/{id}` - Get director details
   - `GET /api/v1/genres` - List genres (with pagination)
   - `GET /api/v1/genres/{id}` - Get genre details

**Note:** If you see empty results, make sure the database is seeded first!