
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "database.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                predicted_traffic REAL NOT NULL,
                traffic_level TEXT NOT NULL,
                weather TEXT,
                road_type TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        conn.commit()


def register_user(username, email, hashed_password):

    try:
        with get_connection() as conn:

            conn.execute("""
                INSERT INTO users
                (username, email, password, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                username,
                email,
                hashed_password,
                datetime.now().isoformat()
            ))

        return True

    except sqlite3.IntegrityError:
        return False


def get_user_by_email(email):

    with get_connection() as conn:

        return conn.execute("""
            SELECT * FROM users WHERE email = ?
        """, (email,)).fetchone()


def save_prediction(
    predicted_traffic,
    traffic_level,
    weather,
    road_type,
    user_id=None
):

    with get_connection() as conn:

        conn.execute("""
            INSERT INTO prediction_history
            (user_id, predicted_traffic, traffic_level,
             weather, road_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            predicted_traffic,
            traffic_level,
            weather,
            road_type,
            datetime.now().isoformat()
        ))


def get_prediction_history(limit=20):

    with get_connection() as conn:

        return conn.execute("""
            SELECT * FROM prediction_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()


if __name__ == "__main__":

    initialize_database()

    print("================================")
    print("SMARTFLOW AI DATABASE")
    print("================================")
    print("Database initialized successfully!")
    print("Users table created.")
    print("Prediction history table created.")
