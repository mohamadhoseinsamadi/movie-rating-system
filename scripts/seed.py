import csv
import json
import random
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal, engine
from app.models.base import Base
from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.rating import MovieRating

# فایل‌های CSV
CSV_PATHS = [
    "scripts/tmdb_5000_movies.csv",
    "scripts/tmdb_5000_credits.csv",
    "tmdb_5000_movies.csv",
    "tmdb_5000_credits.csv"
]


def find_csv(filename):
    for path in CSV_PATHS:
        if path.endswith(filename) and os.path.exists(path):
            return path
    return None


def parse_json_safe(json_str):
    try:
        return json.loads(json_str)
    except:
        return []


def seed_database():
    print("=" * 60)
    print("Starting Database Seeding (TMDB 5000 ETL)")
    print("=" * 60)

    movies_path = find_csv("tmdb_5000_movies.csv")
    credits_path = find_csv("tmdb_5000_credits.csv")

    if not movies_path or not credits_path:
        print("\nERROR: CSV files not found!")
        return

    db = SessionLocal()
    try:
        # 1. Cleanup
        print("\n1. Cleaning up database...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        # 2. Load CSVs
        print(f"\n2. Loading CSV data...")
        with open(movies_path, encoding='utf-8') as f:
            movies_raw = list(csv.DictReader(f))

        with open(credits_path, encoding='utf-8') as f:
            credits_raw = list(csv.DictReader(f))

        credits_map = {row['movie_id']: row for row in credits_raw}

        # 3. Insert Genres (All)
        print("\n3. Extracting Genres...")
        genres_set = set()
        for row in movies_raw:
            for g in parse_json_safe(row.get('genres', '[]')):
                genres_set.add(g['name'])

        genre_objs = {}
        for g_name in genres_set:
            genre = Genre(name=g_name, description="Imported from TMDB")
            db.add(genre)
            genre_objs[g_name] = genre
        db.commit()
        print(f"   Inserted {len(genre_objs)} genres.")

        # 4. Insert Directors (ALL Directors from dataset - Fix for validation)
        print("\n4. Extracting ALL Directors...")
        directors_map = {}  # Name -> Director Object

        # Iterate over ALL credits to capture all directors
        for row in credits_raw:
            crew = parse_json_safe(row['crew'])
            for member in crew:
                if member['job'] == 'Director':
                    d_name = member['name']
                    if d_name and d_name not in directors_map:
                        director = Director(name=d_name, description="Imported from TMDB")
                        db.add(director)
                        directors_map[d_name] = director

        db.commit()  # Commit to save all directors and generate IDs
        print(f"   Inserted {len(directors_map)} directors (Validation Requirement > 1000).")

        # 5. Insert Top 1000 Movies
        print("\n5. Processing Top 1000 Movies...")

        # Sort by popularity/vote_count
        movies_raw.sort(key=lambda x: float(x['vote_count']) if x['vote_count'] else 0, reverse=True)

        movies_limit = 1000
        count = 0

        for row in movies_raw:
            if count >= movies_limit:
                break

            movie_id = row['id']
            credit_row = credits_map.get(movie_id)
            if not credit_row: continue

            # Find Director name
            crew = parse_json_safe(credit_row['crew'])
            director_name = next((m['name'] for m in crew if m['job'] == 'Director'), None)

            # Movie must have a director that we already inserted
            if not director_name or director_name not in directors_map:
                continue

            director_obj = directors_map[director_name]

            # Parse Year
            release_date = row.get('release_date', '')
            release_year = 2000
            if release_date:
                try:
                    release_year = int(release_date.split('-')[0])
                except:
                    pass

            # Cast
            cast_list = parse_json_safe(credit_row['cast'])
            top_cast = [c['name'] for c in cast_list[:3]]
            cast_str = ", ".join(top_cast)

            movie = Movie(
                title=row['title'],
                director_id=director_obj.id,
                release_year=release_year,
                cast=cast_str,
                description="Imported from TMDB Dataset"
            )

            # Genres
            for mg in parse_json_safe(row.get('genres', '[]')):
                if mg['name'] in genre_objs:
                    movie.genres.append(genre_objs[mg['name']])

            db.add(movie)
            count += 1

        db.commit()
        print(f"   Inserted {count} movies.")

        # 6. Ratings
        print("\n6. Generating Ratings...")
        movies = db.query(Movie).all()
        ratings_batch = []
        for movie in movies:
            for _ in range(random.randint(1, 40)):
                ratings_batch.append(MovieRating(
                    movie_id=movie.id,
                    score=random.randint(1, 10),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 1800))
                ))

        db.bulk_save_objects(ratings_batch)
        db.commit()
        print(f"   Inserted {len(ratings_batch)} ratings.")

        print("\n" + "=" * 60)
        print("Seeding Completed Successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
