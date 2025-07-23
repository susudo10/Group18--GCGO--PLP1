from dotenv import load_dotenv
import os

load_dotenv()
import mysql.connector
import os

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
def add_aid_program():
    name = input("Enter aid program name: ")
    aid_type = input("Enter type of aid (e.g., scholarship, fee waiver): ")

    #eligibility criteria
    eligibility_source = input("Enter 'file' to load eligibility from a file or press Enter to type it manually: ").strip().lower()
    if eligibility_source == 'file':
        file_path = input("Enter path to eligibility criteria file (e.g., eligibility_criteria.txt): ").strip()
        try:
            with open(file_path, 'r') as file:
                eligibility = file.read().strip()
        except FileNotFoundError:
            print("File not found. Please make sure the path is correct.")
            return
    else:
        eligibility = input("Enter eligibility criteria: ")

    try:
        funds = float(input("Enter available funds (number): "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    locality = input("Enter target locality: ")

    cursor.execute("""
        INSERT INTO AidPrograms (name, type, eligibility_criteria, available_funds, target_locality)
        VALUES (?, ?, ?, ?, ?)
    """, (name, aid_type, eligibility, funds, locality))

    conn.commit()
    print(" Aid program added successfully.\n")
