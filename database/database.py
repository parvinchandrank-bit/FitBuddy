import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent / "fitbuddy.db"

def connect():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            weight REAL NOT NULL,
            workout_completed INTEGER NOT NULL DEFAULT 0,
            workout_duration INTEGER NOT NULL DEFAULT 0,
            notes TEXT NOT NULL DEFAULT ""
        )""")
        db.commit()

def insert_progress(date, weight, workout_completed, workout_duration, notes):
    init_db()
    with connect() as db:
        cur = db.execute("INSERT INTO progress(date,weight,workout_completed,workout_duration,notes) VALUES(?,?,?,?,?)",
                         (date, weight, int(workout_completed), workout_duration, notes))
        db.commit()
        return dict(db.execute("SELECT * FROM progress WHERE id=?", (cur.lastrowid,)).fetchone())

def get_progress_records():
    init_db()
    with connect() as db:
        return [dict(r) for r in db.execute("SELECT * FROM progress ORDER BY date ASC,id ASC").fetchall()]
