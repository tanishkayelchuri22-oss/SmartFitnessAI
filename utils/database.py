import sqlite3
import os
import hashlib
import secrets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "fitness.db")


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            workout TEXT NOT NULL,
            category TEXT NOT NULL,
            duration REAL NOT NULL,
            weight REAL NOT NULL,
            calories REAL NOT NULL
        )
    """)

    db.commit()
    db.close()


def hash_password(password):
    salt = secrets.token_bytes(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )
    return salt.hex() + ":" + hashed.hex()


def check_password(password, stored):
    salt, saved_hash = stored.split(":")
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt),
        100000
    )
    return secrets.compare_digest(hashed.hex(), saved_hash)


def create_user(name, username, password):
    try:
        db = get_db()
        db.execute(
            "INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
            (name, username, hash_password(password))
        )
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(username, password):
    db = get_db()
    row = db.execute(
        "SELECT name, password FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    db.close()

    if row and check_password(password, row[1]):
        return row[0]

    return None


def save_workout(username, workout, category, duration, weight, calories, date):
    db = get_db()

    db.execute("""
        INSERT INTO workouts
        (username, date, workout, category, duration, weight, calories)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        date,
        workout,
        category,
        duration,
        weight,
        calories
    ))

    db.commit()
    db.close()


def get_workouts(username):
    db = get_db()

    rows = db.execute("""
        SELECT date, workout, category, duration, weight, calories
        FROM workouts
        WHERE username = ?
        ORDER BY id DESC
    """, (username,)).fetchall()

    db.close()
    return rows