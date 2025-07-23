import sqlite3
from datetime import datetime
from db_connection import create_connection

DB_FILE = "san.db"

def get_db_connection():
    """Open an existing database connection."""
    conn = create_connection()
    # conn.row_factory = sqlite3.Row
    return conn


def match_students_to_aid(student_id=None, aid_id=None):
    """
    Match students to aid or aid to students.
    - If student_id is given: return aid programs they qualify for.
    - If aid_id is given: return students who qualify for that program.
    """
    if not (student_id or aid_id):
        raise ValueError("You must provide either student_id or aid_id.")

    conn = get_db_connection()
    c = conn.cursor()

    if student_id:
        # Get the student's profile
        c.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = c.fetchone()
        if not student:
            conn.close()
            return []

        # Find programs matching this student's criteria
        c.execute("""
            SELECT * FROM aid_programs
            WHERE instr(target_localities, ?) > 0
              AND max_income >= ?
              AND min_dependents <= ?
              AND available_funds > 0
        """, (student["locality"], student["income_level"], student["dependents"]))
        matches = c.fetchall()

    else:
        # Get the aid program
        c.execute("SELECT * FROM aid_programs WHERE id = ?", (aid_id,))
        aid = c.fetchone()
        if not aid:
            conn.close()
            return []

        # Find students who match this program's criteria
        c.execute("""
            SELECT * FROM students
            WHERE instr(?, locality) > 0
              AND income_level <= ?
              AND dependents >= ?
              AND aid_status = 'Unfunded'
        """, (aid["target_localities"], aid["max_income"], aid["min_dependents"]))
        matches = c.fetchall()

    conn.close()
    return matches


def allocate_aid(student_id, aid_id, amount):
    """
    Allocate a specific aid amount to a student.
    Updates aid funds and student status.
    """
    conn = get_db_connection()
    c = conn.cursor()

    # Check that student exists and is unfunded
    c.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = c.fetchone()
    if not student:
        conn.close()
        raise ValueError("Student not found.")
    if student["aid_status"] == "Funded":
        conn.close()
        raise ValueError("Student already funded.")

    # Check that aid program exists and has funds
    c.execute("SELECT * FROM aid_programs WHERE id = ?", (aid_id,))
    aid = c.fetchone()
    if not aid:
        conn.close()
        raise ValueError("Aid program not found.")
    if amount > aid["available_funds"]:
        conn.close()
        raise ValueError("Insufficient available funds.")

    # Insert allocation record
    timestamp = datetime.now().isoformat()
    c.execute("""
        INSERT INTO aid_allocations (student_id, aid_id, amount, date_allocated)
        VALUES (?, ?, ?, ?)
    """, (student_id, aid_id, amount, timestamp))

    # Update aid program funds
    c.execute("""
        UPDATE aid_programs
        SET available_funds = available_funds - ?
        WHERE id = ?
    """, (amount, aid_id))

    # Update student status
    c.execute("""
        UPDATE students
        SET aid_status = 'Funded'
        WHERE id = ?
    """, (student_id,))

    conn.commit()
    conn.close()

    return f"Aid of {amount} allocated to student {student_id} from program {aid_id}."
