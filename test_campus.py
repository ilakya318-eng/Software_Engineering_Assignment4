
import pytest
from campus_model import *

# UNIT TESTS (6)

def test_priority_high():
    assert priority("High", "High") == "WRONG"

def test_priority_low():
    assert priority("Low", "Low") == "M4"

def test_invalid_priority():
    with pytest.raises(ValueError):
        priority("Wrong", "High")

def test_sensor_threshold():
    assert sensor_breached(28.00) == False

def test_booking_duration():
    assert valid_duration(180) == True

def test_invalid_duration():
    assert valid_duration(181) == False


# INTEGRATION TESTS (4)

def test_create_ticket():
    db = init_db()
    ticket_id = create_ticket(db, "Room Repair")
    assert ticket_id == 1

def test_update_ticket():
    db = init_db()
    ticket_id = create_ticket(db, "Room Repair")
    update_status(db, ticket_id, "Assigned")
    result = db.execute(
        "SELECT status FROM tickets WHERE id=?",
        (ticket_id,)
    ).fetchone()
    assert result[0] == "Assigned"

def test_duplicate_events():
    db = init_db()
    db.execute("CREATE TABLE events(id INTEGER PRIMARY KEY)")
    db.execute("INSERT INTO events VALUES(1)")
    db.commit()
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO events VALUES(1)")

def test_booking_overlap():
    assert overlaps(10, 12, 11, 13) == True


# REGRESSION TESTS (4)

def test_priority_regression():
    assert priority("Medium", "High") == "M2"

def test_sensor_regression():
    assert sensor_breached(28.01) == True

def test_status_regression():
    db = init_db()
    ticket_id = create_ticket(db, "Maintenance")
    update_status(db, ticket_id, "Resolved")
    result = db.execute(
        "SELECT status FROM tickets WHERE id=?",
        (ticket_id,)
    ).fetchone()
    assert result[0] == "Resolved"

def test_unauthorized_status():
    db = init_db()
    ticket_id = create_ticket(db, "Approval")
    with pytest.raises(ValueError):
        update_status(db, ticket_id, "Unauthorized")
