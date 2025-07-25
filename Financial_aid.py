import os
from dotenv import load_dotenv
import mysql.connector

# Import  connection function
from db_connection import create_connection

load_dotenv()

# Optional: direct test connection
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

#  Create AidPrograms
def create_aid_programs_table():
    connection = create_connection()
    if connection is None:
        print("❌ Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AidPrograms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                type VARCHAR(50) NOT NULL,
                eligibility_criteria TEXT,
                available_funds FLOAT,
                target_locality VARCHAR(100)
            )
        """)
        connection.commit()

    except mysql.connector.Error as e:
        print(f"❌ Error creating table: {e}")
    finally:
        cursor.close()
        connection.close()

# 1. Add Aid Program
def add_aid_program():
    conn = create_connection()
    if conn is None:
        print("❌ Could not connect to the database.")
        return

    cursor = conn.cursor()

    name = input("Enter aid program name: ")

    # Validate aid type input (must be 's' or 'f')
    while True:
        aid_type_input = input("Enter type of aid - (s) for scholarship or (f) for fee waiver: ").lower()
        if aid_type_input == 's':
            aid_type = "scholarship"
            break
        elif aid_type_input == 'f':
            aid_type = "fee waiver"
            break
        else:
            print("❌ Invalid input. Please enter 's' or 'f'.")

    # Eligibility input from file or manually
    eligibility_input = input("Enter 'file' to load eligibility from a file or press Enter to type it manually: ")
    if eligibility_input.lower() == 'file':
        file_path = input("Enter path to eligibility criteria file (e.g., eligibility_criteria.txt): ")
        try:
            with open(file_path, 'r') as f:
                eligibility = f.read().strip()
        except FileNotFoundError:
            print("File not found. Please make sure the path is correct.")
            return
    else:
        eligibility = input("Enter eligibility criteria: ")

    # Prompt for funds in dollars
    while True:
        try:
            funds = float(input("Enter available funds in dollars (e.g., 5000): $"))
            break
        except ValueError:
            print("❌ Invalid amount. Please enter a valid number.")

    locality = input("Enter target locality: ")

    try:
        cursor.execute("""
            INSERT INTO AidPrograms (name, type, eligibility_criteria, available_funds, target_locality)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, aid_type, eligibility, funds, locality))
        conn.commit()
        print("✅ Aid program added successfully.")
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        cursor.close()
        conn.close()
# 2. View aid programs

import mysql.connector
from db_connection import create_connection

def view_aid_programs(locality=None):

    connection = create_connection()

    if connection:
        try:
            cursor = connection.cursor()
            if locality:
                query = "SELECT * FROM AidPrograms WHERE target_locality = %s"
                cursor.execute(query, (locality,))
            else:
                cursor.execute("SELECT * FROM AidPrograms")

            programs = cursor.fetchall()
            if programs:
                headers = ["ID", "Name", "Type", "Eligibility Criteria", "Available Funds", "Target Locality"]
                print("\n--- List of Aid Programs ---")
                print(tabulate(programs, headers=headers, tablefmt="fancy_grid"))
            else:
                print("⚠️ No aid programs found.")
        except mysql.connector.Error as e:
            print(f"❌ Error fetching aid programs: {e}")
        finally:
        cursor.close()
        connection.close()
# 3. Update an aid program by ID
def update_aid_program():
    connection = create_connection()
    if connection is None:
        print("❌ Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()
        program_id = input("Enter ID of the aid program to update: ")

        # Check if program exists
        cursor.execute("SELECT * FROM AidPrograms WHERE id = %s", (program_id,))
        program = cursor.fetchone()
        if not program:
            print("❌ Aid program not found.")
            return

        print("Enter new details (press Enter to keep current value):")
        print("Type options: (s) for scholarship, (f) for fee waiver")

        # Validate new type
        while True:
            new_type_input = input(f"Type [{program[2]}]: ").strip().lower()
            if not new_type_input:
                new_type = program[2]  # Keep existing
                break
            elif new_type_input == 's':
                new_type = "scholarship"
                break
            elif new_type_input == 'f':
                new_type = "fee waiver"
                break
            else:
                print("❌ Invalid input. Please enter 's' or 'f'.")

        new_eligibility = input(f"Eligibility [{program[3]}]: ") or program[3]


