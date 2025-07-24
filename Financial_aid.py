import os
from dotenv import load_dotenv
import mysql.connector

# Import  connection function
from db_connection import create_connection

load_dotenv()


conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)


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
