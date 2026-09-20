import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_FILE = os.path.join(BASE_DIR, "data", "workout_history.csv")

FIELDS = [
    "date",
    "workout",
    "category",
    "duration",
    "weight",
    "calories"
]

def save_workout(workout, category, duration, weight, calories):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    file_exists = os.path.exists(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)

        if not file_exists or os.path.getsize(HISTORY_FILE) == 0:
            writer.writeheader()

        writer.writerow({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "workout": workout,
            "category": category,
            "duration": duration,
            "weight": weight,
            "calories": round(calories)
        })