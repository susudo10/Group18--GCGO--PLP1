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
        self.cursor.execute(
            """
            """,
        )
        self.connection.commit()
        print(f"Student '{student.name}' added successfully.✅")


        conditions = []
        values = []

        if filter_by_region:
            conditions.append("region = %s")
            values.append(filter_by_region)

        if filter_by_status:
            conditions.append("aid_status = %s")
            values.append(filter_by_status)

        if conditions:

        results = self.cursor.fetchall()

        for row in results:
            print(row)

    # Method to update the student profile details



        #Join the update strings into one SQL statement

        # Executing the query and committing the updates
        self.connection.commit()
        print(f"Student {student_id} updated successfully.")

    # Method to delete the student record
    def delete_student(self, student_id):
        self.connection.commit()
        print("Student deleted successfully.")
