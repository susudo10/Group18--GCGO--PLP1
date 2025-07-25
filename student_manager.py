#!/usr/bin/python3
"""
This module defines a StudentManager class with properties and methods
to add, view, update and delete students.
It is basically the controller that manages the collection student objects and links to the database.
"""

# First importing the sql database and the class student.
import mysql.connector
from student import Student # Assuming student class is in student.py
import os
from dotenv import load_dotenv

load_dotenv() #Loading the .env variables into the script


class StudentManager:
    """ Defines the class StudentManager."""
    def __init__(self):
        """ This connects to the aiven databse."""
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )
        self.cursor = self.connection.cursor()


    # Method to add a student
    def add_student(self, student: Student):
        print("Connected to DB from student_manager: ", self.connection.database)
        # Debug print before the SQL query
        print("Inserting student with values: ")
        print("Name:", student.name)
        print("Contact:", student.contact)
        print("DOB:", student.dob)
        print("Income:", student.income)
        print("Dependents:", student.dependents)
        print("Region:", student.region)
        print("School:", student.school)

        """Adds a new student to the database."""
        self.cursor.execute(
            """
            INSERT INTO Students (name, contact, dob, income, dependents, region, school) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                student.name,
                student.contact,
                student.dob,
                student.income,
                student.dependents,
                student.region,
                student.school              
            )
        )
        self.connection.commit()
        print(f"Student '{student.name}' added successfully.✅")

    # Method to view specific student details by ID
    def view_student_details(self, student_id):
        try:
            self.cursor.execute("SELECT * FROM Students WHERE id = %s", (student_id,)) # Comma!
            student = self.cursor.fetchone()
            if student:
                print("\n--- Student Details ---")
                print(student)
            else:
                print(f"No student found with ID {student_id}😔.")
        except mysql.connector.Error as e:
            print(f"Error retrieving student: {e}")

    # Method to filter a student
    def filter_students(self, filter_by_region=None, filter_by_status=None):
        query3 = "SELECT * FROM Students"
        conditions = []
        values = []

        if filter_by_region:
            conditions.append("region = %s")
            values.append(filter_by_region)

        if filter_by_status:
            conditions.append("aid_status = %s")
            values.append(filter_by_status)

        if conditions:
            query3 += " WHERE " + " AND ".join(conditions)

        self.cursor.execute(query3, values)
        results = self.cursor.fetchall()

        for row in results:
            print(row)

    # Method to Update Student Information
    def update_student_info(self, student_id, field, new_value):
        try:
            if field not in ['name', 'contact', 'dob', 'school', 'region', 'income', 'dependents', 'aid_status']:
                print("Invalid field name.")
                return
            query = f"UPDATE Students SET {field} = %s WHERE id = %s"
            self.cursor.execute(query, (new_value, student_id))
            self.connection.commit()
            print(" Student info updated successfully.")
        except mysql.connector.Error as e:
            print(f"Error updating student info: {e}")
    # Method to update the student profile details
    def update_student(self, student_id, updates : dict):
        """
        This defines the property to update student details in updates dict.
        
        Args:
        student_id(INT): The ID of the student to update.
        updates (dict): A dictionary of field names and their new values.
                        e.g, {'name': 'Jane Doe', 'income': 30000}
        """
        if not updates:
            print("No updates provided.")
            return 
        
        # Creating a SET clause which is dynamic through Looking over dictionary of fields which can be updated
        set_clause = ", ".join([f"{field} = %s" for field in updates.keys()])
        values = list(updates.values())
        values.append(student_id)


        #Join the update strings into one SQL statement
        query1 = f"UPDATE Students SET {set_clause} WHERE id = %s"

        # Executing the query and committing the updates
        try:
            self.cursor.excute(query1, values)
            self.connection.commit()
            print(f"Student {student_id} updated successfully.")
        except Exception as e:
            print(f"Error updating student: {e}")

    # Method to list all students
    def list_all_students(self):
        try:
            self.cursor.execute("SELECT * FROM Students")
            students = self.cursor.fetchall()
            if students:
                print("\n--- All Students ---")
                for student in students:
                    print(student)
            else:
                print("No student records found.")
        except mysql.connector.Error as e:
            print(f"Error retrieving students: {e}")

    # Method to delete the student record
    def delete_student(self, student_id):
        query2 = "DELETE FROM Students WHERE id = %s"
        self.cursor.execute(query2, (student_id,))
        self.connection.commit()
        print("Student deleted successfully.")

def prompt_and_add_student():
    print("Welcome, we are creating a profile for you...")
    name = input("Please may you enter your full name: ")
    contact = input("Enter your contact number: ")
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    income = float(input("Please you enter the average income in your household monthly (RWF) ending with .00: "))
    dependents = int(input("Enter number of dependents in your household "
    "(don't worry it means the number of people who depend on that income): "))
    region = input("Enter your region: ")
    school = input("Enter your school: ")
    manager = StudentManager()

    student = Student(None, name, contact, dob, income, dependents, region, school)

    manager.add_student(student)

if __name__ == "__main__":
    manager = StudentManager()

    # List all students
    print("\n Testing: List All Students")
    manager.list_all_students()

    # View one student by ID
    print("\n Testing: View Student Details")
    manager.view_student_details(1)  # Use a valid ID from your DB

    # Update student info
    print("\n Testing: Update Student Info")
    manager.update_student_info(1, "contact", "0788888888")  # Use a valid ID and field

