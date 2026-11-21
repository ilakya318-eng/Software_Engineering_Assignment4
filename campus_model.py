
import sqlite3

MATRIX = {
    ("High", "High"): "M1",
    ("High", "Medium"): "M2",
    ("High", "Low"): "M3",
    ("Medium", "High"): "M2",
    ("Medium", "Medium"): "M3",
    ("Medium", "Low"): "M4",
    ("Low", "High"): "M3",
    ("Low", "Medium"): "M4",
    ("Low", "Low"): "M4"
}

def priority(impact, urgency):
    if (impact, urgency) not in MATRIX:
        raise ValueError("Invalid input")
    return MATRIX[(impact, urgency)]

def sensor_breached(value):
    return value > 28.0

def valid_duration(minutes):
    return 0 < minutes <= 180

def overlaps(s1, e1, s2, e2):
    return s1 < e2 and s2 < e1

def create_ticket(db, title):
    if not title.strip():
        raise ValueError("Title required")
    cur = db.execute(
        "INSERT INTO tickets(title, status) VALUES(?, ?)",
        (title, "New")
    )
    db.commit()
    return cur.lastrowid

def update_status(db, ticket_id, status):
    allowed = ["New", "Assigned", "In Progress",
               "Resolved", "Closed"]
    if status not in allowed:
        raise ValueError("Invalid status")
    db.execute("UPDATE tickets SET status=? WHERE id=?",
               (status, ticket_id))
    db.commit()

def init_db():
    db = sqlite3.connect(":memory:")
    db.execute("""
        CREATE TABLE tickets(
            id INTEGER PRIMARY KEY,
            title TEXT,
            status TEXT
        )
    """)
    return db
