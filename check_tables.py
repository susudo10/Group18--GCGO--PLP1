import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

connection = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="defaultdb"
)

cursor = connection.cursor()
cursor.execute("SHOW TABLES")

tables = cursor.fetchall()
print("Tables in your database:")
for table in tables:
    print(table[0])

cursor.close()
connection.close()
