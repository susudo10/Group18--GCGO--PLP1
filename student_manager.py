#!/usr/bin/python3
"""
This module defines a StudentManager class with properties and methods
to add, view, update and delete students.
It is basically the controller that manages the collection student objects and links to the database.
"""

"""First importing the sql database and the class student."""
import mysql.connector
from student import Student # Assuming student class is in student.py
import os
from dotenv import load_dotenv

load_dotenv


class StudentManager:
    """ Defines the class Student."""
    def __init__(self, connection, cursor):
        """ This connects to the aiven databse."""
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )
        self.cursor = self.connection.cursor()


    @property
    def add_Student(self, student: Student):
        self.cursor.execute(
            "INSERT INTO students (name, contact, school, income, dob, dependents, region) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, contact, school, income, dob, dependants, region)
        )
        self.connection.commit()
        print(f"Student '{student.name}' added successfully.✅")


    @property
    def view_students(self, filter_by_region=None, filter_by status=None):
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

    @property

