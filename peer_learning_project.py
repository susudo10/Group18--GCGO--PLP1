import time
import sqlite3
from datetime import datetime

DB_FILE = "san.db"


def get_db_connection():
    """Connect to the database and return a connection object."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def match_students_to_aid(student_id=None, aid_id=None):
    """
    Find suitable aid programs for a student or find eligible students for an aid program.
    """
    if not (student_id or aid_id):
        raise ValueError("You must provide either a student ID or an aid program ID.")

    with get_db_connection() as conn:
        c = conn.cursor()

        if student_id:
            c.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            student = c.fetchone()
            if not student:
                print("No student found.")
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
                return []

            c.execute("""
                SELECT * FROM students
                WHERE instr(?, locality) > 0
                  AND income_level <= ?
                  AND dependents >= ?
                  AND aid_status = 'Unfunded'
            """, (aid["target_localities"], aid["max_income"], aid["min_dependents"]))
            matches = c.fetchall()

    return matches


def allocate_aid(student_id, aid_id, amount):
    """
    Allocate a specific aid amount to a student and update records.
    """
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
            raise ValueError("Not enough funds available in this program.")

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

    return f"Aid of {amount} has been allocated to student {student_id} from program {aid_id}."


def display_matching_menu():
    """
    Display options for matching students and aid programs.
    """
    print("\n--- Matching Menu ---")
    print("1. Find aid programs for a student")
    print("2. Find eligible students for an aid program")
    print("3. Back to main menu")

    choice = input("Enter your choice: ")

    if choice == "1":
        student_id = input("Enter student ID: ")
        matches = match_students_to_aid(student_id=int(student_id))
        if matches:
            print("\nMatching Aid Programs:")
            for program in matches:
                print(dict(program))
        else:
            print("No matching aid programs found.")
    elif choice == "2":
        aid_id = input("Enter aid program ID: ")
        matches = match_students_to_aid(aid_id=int(aid_id))
        if matches:
            print("\nEligible Students:")
            for student in matches:
                print(dict(student))
        else:
            print("No eligible students found.")
    elif choice == "3":
        return
    else:
        print("Invalid choice. Please try again.")


def display_allocation_menu():
    """
    Display options for allocating aid.
    """
    print("\n--- Allocation Menu ---")
    student_id = input("Enter student ID: ")
    aid_id = input("Enter aid program ID: ")
    amount = float(input("Enter amount to allocate: "))

    try:
        result = allocate_aid(int(student_id), int(aid_id), amount)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")


def main_menu():
    """
    Main command-line menu for the Student Aid Network.
    """
    while True:
        print("\n=== Student Aid Network ===")
        print("1. Match Students to Aid Programs")
        print("2. Allocate Aid to a Student")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_matching_menu()
        elif choice == "2":
            display_allocation_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
