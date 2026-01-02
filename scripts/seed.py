# scripts/seed.py
import os
import psycopg2
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def seed_database():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("🗑️ Clearing existing data...")
        cursor.execute("TRUNCATE TABLE movies, users, ratings RESTART IDENTITY CASCADE;")
        
        print("👤 Seeding users...")
        users_data = []
        for i in range(1, 101):
            users_data.append((f"user{i}", f"user{i}@example.com"))
        
        cursor.executemany(
            "INSERT INTO users (username, email) VALUES (%s, %s);",
            users_data
        )
        
        print("🎬 Seeding movies...")
        movie_titles = [
            "The Matrix", "Inception", "Interstellar", "The Dark Knight", "Pulp Fiction",
            "Fight Club", "Forrest Gump", "The Godfather", "The Shawshank Redemption",
            # ... اضافه کن بقیه فیلم‌ها
        ]
        
        # اگر 1000 فیلم می‌خواهی، باید لیست کامل‌تری داشته باشی
        movies_data = []
        for i in range(1, 1001):
            title = f"Movie {i}" if i > len(movie_titles) else movie_titles[i-1]
            year = random.randint(1990, 2023)
            rating = round(random.uniform(1.0, 10.0), 1)
            movies_data.append((title, year, rating))
        
        cursor.executemany(
            "INSERT INTO movies (title, release_year, rating) VALUES (%s, %s, %s);",
            movies_data
        )
        
        print("⭐ Seeding ratings...")
        ratings_data = []
        for user_id in range(1, 101):
            for _ in range(20):  # هر کاربر 20 امتیاز می‌دهد
                movie_id = random.randint(1, 1000)
                score = random.randint(1, 10)
                ratings_data.append((user_id, movie_id, score))
        
        cursor.executemany(
            "INSERT INTO ratings (user_id, movie_id, score) VALUES (%s, %s, %s);",
            ratings_data
        )
        
        conn.commit()
        print("✅ Database seeded successfully!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Seeding failed: {e}")

if __name__ == "__main__":
    seed_database()