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
    """ Defines the class Student."""
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
        """Adds a new student to the database."""
        self.cursor.execute(
            """
            INSERT INTO students (name, contact, school, income, dob, dependents, region) 
            VALUES (%s, %s, %s, %s, %s, %s, %s),
            """,
            (
                student.name,
                student.contact,
                student.school,
                student.income,
                student.dob,
                student.dependents,
                student.region
            )
        )
        self.connection.commit()
        print(f"Student '{student.name}' added successfully.✅")


    # Method to view a student
    def view_students(self, filter_by_region=None, filter_by_status=None):
        query = "SELECT * FROM students"
        conditions = []
        values = []

        if filter_by_region:
            conditions.append("region = %s")
            values.append(filter_by_region)

        if filter_by_status:
            conditions.append("aid_status = %s")
            values.append(filter_by_status)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        self.cursor.execute(query, values)
        results = self.cursor.fetchall()

        for row in results:
            print(row)

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
        query = f"UPDATE students SET {set_clause} WHERE id = %s"

        # Executing the query and committing the updates
        try:
            self.cursor.excute(query, values)
            self.connection.commit()
            print(f"Student {student_id} updated successfully.")
        except Exception as e:
            print(f"Error updating student: {e}")

    # Method to delete the student record
    def delete_student(self, student_id):
        query = "DELETE FROM students WHERE id = %s"
        self.cursor.execute(query, (student_id,))
        self.connection.commit()
        print("Student deleted successfully.")
