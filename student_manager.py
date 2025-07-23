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
    def add_Student(self, student: Student):
        self.cursor.execute(
            """
            INSERT INTO students (name, contact, school, income, dob, dependents, region) 
            VALUES (%s, %s, %s, %s, %s, %s, %s),
            """,
            (student.name, student.contact, student.school, student.income, student.dob, student.dependents, student.region)
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
    def update_student(self, student_id, update_data):
        """This defines the property to update student details on their profile."""
        updates = []
        values = []

        # Look over dictionary of fields which can be updated
        for key, value in update_data.items():
            updates.append(f"{key} = %s") #e.g "contact = %s"
            values.append(value)          #e.g 0779234567

        values.append(student_id) # This is the student we're updating for

        #Join the update strings into one SQL statement
        query = f"UPDATE students SET {', '.join(updates)} WHERE id = %s"

        # Executing the query and committing the updates
        self.cursor.excute(query, values)
        self.connection.commit()
        print(f"Student {student_id} updated successfully.")

    # Method to delete the student record
    def delete_student(self, student_id):
        query = "DELETE FROM students WHERE id = %s"
        self.cursor.execute(query, (student_id,))
        self.connection.commit()
        print("Student deleted successfully.")
