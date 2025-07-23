# File: main.py
import sqlite3
from database import create_connection, create_tables
from student import add_student, view_students, update_student, delete_student
from aid_program import add_aid_program, view_aid_programs, update_aid_program
from matching import match_students_to_aid, allocate_aid
from reporting import generate_report

def display_main_menu():
    """Display the main menu options"""
    print("\n" + "=" * 50)
    print("STUDENT AID NETWORK - Local Authority Portal")
    print("=" * 50)
    print("1. Register New Student")
    print("2. View Students")
    print("3. Manage Aid Programs")
    print("4. Match Students to Aid")
    print("5. Allocate Aid to Student")
    print("6. Update Student Record")
    print("7. Generate Reports")
    print("8. Exit")
    print("=" * 50)
    return input("Enter your choice (1-8): ")

def view_students_menu(conn):
    """Submenu for viewing students"""
    print("\n--- View Students ---")
    print("1. View All Students")
    print("2. Filter by Region")
    print("3. Filter by Need Level")
    print("4. Back to Main Menu")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        view_students(conn)
    elif choice == '2':
        region = input("Enter region: ")
        view_students(conn, "region", region)
    elif choice == '3':
        need_level = input("Enter need level (Low/Medium/High): ").capitalize()
        view_students(conn, "need", need_level)

def aid_programs_menu(conn):
    """Submenu for managing aid programs"""
    print("\n--- Aid Program Management ---")
    print("1. Add New Aid Program")
    print("2. View Aid Programs")
    print("3. Update Aid Program")
    print("4. Back to Main Menu")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        add_aid_program(conn)
    elif choice == '2':
        region = input("Filter by region (leave blank for all): ")
        view_aid_programs(conn, "region", region) if region else view_aid_programs(conn)
    elif choice == '3':
        update_aid_program(conn)

def reports_menu(conn):
    """Submenu for generating reports"""
    print("\n--- Generate Reports ---")
    print("1. Student Report")
    print("2. Aid Programs Report")
    print("3. Allocations Report")
    print("4. Back to Main Menu")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        generate_report(conn, "students")
    elif choice == '2':
        generate_report(conn, "aid")
    elif choice == '3':
        generate_report(conn, "allocations")

def main():
    """Main application function"""
    # Initialize database
    conn = create_connection()
    if conn is not None:
        create_tables(conn)
        print("Database initialized successfully")
    else:
        print("Error! Cannot create database connection.")
        return
    
    print("\n" + "=" * 50)
    print("Welcome to Student Aid Network")
    print("Empowering local authorities to support needy students")
    print("=" * 50)
    
    # Main application loop
    while True:
        choice = display_main_menu()
        
        if choice == '1':  # Register New Student
            add_student(conn)
        elif choice == '2':  # View Students
            view_students_menu(conn)
        elif choice == '3':  # Manage Aid Programs
            aid_programs_menu(conn)
        elif choice == '4':  # Match Students to Aid
            match_students_to_aid(conn)
        elif choice == '5':  # Allocate Aid to Student
            allocate_aid(conn)
        elif choice == '6':  # Update Student Record
            update_student(conn)
        elif choice == '7':  # Generate Reports
            reports_menu(conn)
        elif choice == '8':  # Exit
            print("\nThank you for using the Student Aid Network. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1-8.")
    
    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()