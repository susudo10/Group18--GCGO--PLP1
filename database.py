# File: database.py
import sqlite3
from sqlite3 import Error

def create_connection():
    """Create a database connection to SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect('student_aid_network.db')
        print(f"Connected to SQLite database version {sqlite3.version}")
        return conn
    except Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Create tables for students, aid programs, and allocations"""
    sql_create_students_table = """ CREATE TABLE IF NOT EXISTS students (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        age INTEGER,
                                        school TEXT,
                                        grade TEXT,
                                        region TEXT,
                                        household_income REAL,
                                        dependents INTEGER,
                                        need_level TEXT,
                                        contact TEXT
                                    ); """
    
    sql_create_aid_programs_table = """ CREATE TABLE IF NOT EXISTS aid_programs (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        type TEXT,
                                        description TEXT,
                                        max_amount REAL,
                                        available_amount REAL,
                                        region TEXT
                                    ); """
    
    sql_create_allocations_table = """ CREATE TABLE IF NOT EXISTS allocations (
                                        id INTEGER PRIMARY KEY,
                                        student_id INTEGER NOT NULL,
                                        program_id INTEGER NOT NULL,
                                        amount REAL,
                                        status TEXT DEFAULT 'Pending',
                                        FOREIGN KEY (student_id) REFERENCES students (id),
                                        FOREIGN KEY (program_id) REFERENCES aid_programs (id)
                                    ); """
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_students_table)
        cursor.execute(sql_create_aid_programs_table)
        cursor.execute(sql_create_allocations_table)
        conn.commit()
    except Error as e:
        print(e)