# 🎬 Movie Rating System API

A robust, production-ready RESTful API for managing movies, directors, genres, and user ratings. This system is designed with **Layered Architecture** and **Observability** principles in mind, utilizing **FastAPI** and **PostgreSQL**.

> **Phases Completed:**
> *   ✅ **Phase 1:** Back-End Logic, CRUD, Database Design, Layered Architecture.
> *   ✅ **Phase 2:** Logging, Observability, Structured Error Handling.

---

## 🚀 Features

*   **Movie Management:** Create, Update, Delete, and Retrieve movies.
*   **Advanced Search & Filtering:** Filter movies by Title, Release Year, and Genre with Pagination.
*   **Director & Genre Management:** Manage metadata for movies.
*   **Rating System:** Users can rate movies (1-10). The system automatically calculates Average Rating and Rating Count.
*   **Data Consistency:** Cascade deletions ensure no orphaned data (e.g., deleting a movie deletes its ratings).
*   **ETL Seeding:** Python script to load real-world data from the TMDB 5000 dataset.
*   **Structured Logging:** Professional logging configuration (INFO, WARNING, ERROR) for monitoring.
*   **Standardized Responses:** Unified JSON structure for both Success and Error responses.

---

## 🛠️ Tech Stack

*   **Language:** Python 3.9+
*   **Framework:** FastAPI
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy
*   **Validation:** Pydantic
*   **Server:** Uvicorn

---

## 💾 Database Seeding (ETL)

1.  **Download Data:**
    Download `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` from [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).

2.  **Place Files:**
    Put the CSV files inside the `scripts/` folder.

3.  **Run Seeder:**
    ```bash
    python scripts/seed.py
    ```

---

## ▶️ Running the Application

Start the server using Uvicorn:

```bash
uvicorn app.main:app --reload
