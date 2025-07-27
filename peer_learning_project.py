# Peer Learning project: Student Aid Network
# This script manages a student aid network, allowing students to find aid programs
# It uses SQLite for data storage.

import time
import sys
import sqlite3
from datetime import datetime
from db_connection import create_connection
from db_connect import connect_to_database

DB_FILE = "san.db"

# Setup database
def setup_db():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            locality TEXT,
            income_level REAL,
            dependents INTEGER,
            aid_status TEXT DEFAULT 'Unfunded'
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS aid_programs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            target_localities TEXT,
            max_income REAL,
            min_dependents INTEGER,
            available_funds REAL
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS aid_allocations (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            aid_id INTEGER,
            amount REAL,
            date_allocated TEXT
        )
        """)
        conn.commit()

# Get a database connection
def get_db_connection():
    """Connect to the database and return a connection object."""
    conn = connect_to_database()
    conn.row_factory = sqlite3.Row
    return conn

# Match students to aid programs or vice versa
def match_students_to_aid(student_id=None, aid_id=None):
    """Find suitable aid programs for a student or eligible students for a program."""
    if not (student_id or aid_id):
        raise ValueError("Provide either a student ID or an aid program ID.")
    time.sleep(1)

    with get_db_connection() as conn:
        c = conn.cursor()

        # If student_id is provided, find matching aid programs
        if student_id:
            c.execute("SELECT * FROM Students WHERE id = ?", (student_id))
            student = c.fetchone()
            if not student:
                print("No student found.")
                time.sleep(1)
                return []

            c.execute("""
                SELECT * FROM aid_programs
                WHERE instr(target_localities, ?) > 0
                  AND max_income >= ?
                  AND min_dependents <= ?
                  AND available_funds > 0
            """, (student["locality"], student["income_level"], student["dependents"]))
            matches = c.fetchall()

        else:
            c.execute("SELECT * FROM aid_programs WHERE id = ?", (aid_id,))
            aid = c.fetchone()
            if not aid:
                print("No aid program found.")
                time.sleep(1)
                return []

            c.execute("""
                SELECT * FROM students
                WHERE instr(locality, ?) > 0
                  AND income_level <= ?
                  AND dependents >= ?
                  AND aid_status = 'Unfunded'
            """, (aid["target_localities"], aid["max_income"], aid["min_dependents"]))
            matches = c.fetchall()

    return matches

# Allocate aid to a student
def allocate_aid(student_id, aid_id, amount):
    """Allocate aid to a student and update records."""
    with get_db_connection() as conn:
        c = conn.cursor()

        c.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = c.fetchone()
        if not student:
            raise ValueError("Student not found.")
        if student["aid_status"] == "Funded":
            raise ValueError("Student is already funded.")

        c.execute("SELECT * FROM aid_programs WHERE id = ?", (aid_id,))
        aid = c.fetchone()
        if not aid:
            raise ValueError("Aid program not found.")
        if amount > aid["available_funds"]:
            raise ValueError("Not enough funds available...")

        timestamp = datetime.now().isoformat()

        c.execute("""
            INSERT INTO aid_allocations (student_id, aid_id, amount, date_allocated)
            VALUES (?, ?, ?, ?)
        """, (student_id, aid_id, amount, timestamp))

        c.execute("""
            UPDATE aid_programs
            SET available_funds = available_funds - ?
            WHERE id = ?
        """, (amount, aid_id))

        c.execute("""
            UPDATE students
            SET aid_status = 'Funded'
            WHERE id = ?
        """, (student_id,))

        conn.commit()

    return f"Aid of {amount} allocated to student {student_id} from program {aid_id}."

# Display matching aid programs or eligible students
def display_matching_menu():
    """Menu for aid matching."""
    print("\n--- Matching Menu ---")
    print("1. Find aid programs for a student")
    print("2. Find eligible students for an aid program")
    print("3. Back to main menu")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        student_id = input("Enter student ID: ").strip()
        if not student_id.isdigit():
            print("Invalid student ID. Must be numeric.")
            return
        matches = match_students_to_aid(student_id=int(student_id))
        if matches:
            print("\nMatching Aid Programs:")
            for program in matches:
                print(dict(program))
        else:
            print("No matching aid programs found.")
            time.sleep(2)
        input("Press Enter to continue...")
    
    elif choice == "2":
        aid_id = input("Enter aid program ID: ").strip()
        if not aid_id.isdigit():
            print("Invalid aid ID. Must be numeric.")
            return
        matches = match_students_to_aid(aid_id=int(aid_id))

        # If matches found, display them
        if matches:
            print("\nEligible Students:")
            for student in matches:
                print(dict(student))
        else:
            print("No eligible students found.")
            time.sleep(2)
        input("\nPress Enter to return to the main menu...")

    elif choice == "3":
        return
    else:
        print("Invalid choice. Try again.")
        time.sleep(1)

# Display aid allocation menu
def display_allocation_menu():
    """Menu for aid allocation."""
    print("\n--- Allocation Menu ---")
    student_id = input("Enter student ID: ").strip()
    aid_id = input("Enter aid program ID: ").strip()
    amount_input = input("Enter amount to allocate: ").strip()

    # Validate inputs
    if not student_id.isdigit() or not aid_id.isdigit():
        print("Student and Aid IDs must be numeric(numbers).")
        return

    try:
        amount = float(amount_input)
    except ValueError:
        print("Invalid amount. Must be a number.")
        return

    try:
        result = allocate_aid(int(student_id), int(aid_id), amount)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
        time.sleep(1)
    input("Press Enter to return to the main menu...")

# Main menu loop
def main_menu():
    """Main menu loop."""
    while True:
        print("\n=== Student Aid Network ===")
        print("1. Match Students to Aid Programs")
        print("2. Allocate Aid to a Student")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_matching_menu()
        elif choice == "2":
            display_allocation_menu()
        elif choice == "3":
            print("Goodbye!...")
            time.sleep(1)
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    setup_db()  # Ensure database is set up
    main_menu()
