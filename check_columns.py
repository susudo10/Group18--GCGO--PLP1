#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def list_student_columns():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT"))
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("DESCRIBE Students;")
            columns = cursor.fetchall()

            print("Columns in 'Students' table:")
            for col in columns:
                print(col[0])  # Only print the column name (field)

            cursor.close()
        else:
            print("Failed to connect to the database.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Run the function
list_student_columns()
