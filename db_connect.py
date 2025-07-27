import mysql.connector
from dotenv import load_dotenv

import os
load_dotenv()


def connect_to_database():
    """Connect to the MySQL database and return the connection object."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT"),
            ssl_disabled=False
        )
        if conn.is_connected():
            db_infor = conn.get_server_info
            db_name = conn.database
            print(f"Connected to MySQL database {db_infor} at {db_name}")
            return conn
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None