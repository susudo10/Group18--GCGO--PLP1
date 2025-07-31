#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

def create_connection():
    try: 
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT"))
        )

        if connection.is_connected():
            print("Connection to the database was successful")
            print(f"Database name: {connection.database}")
            print(f"Server version: {connection.server_info}")
            print(f"Connected to: ", connection.database)
            return connection
        else:
            print("Connection to the database failed")
            return None
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    
 # Creating the table students   
def create_students_table():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor() 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    contact VARCHAR(50),
                    dob DATE,
                    school VARCHAR(100),
                    region VARCHAR(100),
                    income DECIMAL(10, 2),
                    dependents INT,
                    aid_status VARCHAR(20) DEFAULT 'pending',
                    amount_needed DECIMAL(10, 2),
                    priority_index INT DEFAULT 0
                );
            """)
            connection.commit()
            print("✅ Students table created successfully.")
        except mysql.connector.Error as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("⚠️ Failed to connect. Table not created.")

# Run it
create_students_table()
