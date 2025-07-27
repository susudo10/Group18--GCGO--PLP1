import sqlite3

conn = sqlite3.connect("san.db")
c = conn.cursor()

# Create students table
c.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    locality TEXT,
    income_level INTEGER,
    dependents INTEGER,
    aid_status TEXT DEFAULT 'Unfunded'
)
""")

# Create aid_programs table
c.execute("""
CREATE TABLE IF NOT EXISTS aid_programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    target_localities TEXT,
    max_income INTEGER,
    min_dependents INTEGER,
    available_funds REAL
)
""")

# Create aid_allocations table
c.execute("""
CREATE TABLE IF NOT EXISTS aid_allocations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    aid_id INTEGER,
    amount REAL,
    date_allocated TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(aid_id) REFERENCES aid_programs(id)
)
""")

# Seed with sample students
students = [
    ("Amina", "Kigali", 25000, 3, "Unfunded"),
    ("Eric", "Musanze", 18000, 2, "Unfunded"),
    ("Claudine", "Gisozi", 22000, 4, "Unfunded"),
]
c.executemany("INSERT INTO students (name, locality, income_level, dependents, aid_status) VALUES (?, ?, ?, ?, ?)", students)

# Seed with sample aid programs
aid_programs = [
    ("Water Access Initiative", "Kigali;Gisozi", 30000, 2, 5000),
    ("Youth Support Fund", "Musanze;Rubavu", 25000, 1, 3000),
]
c.executemany("INSERT INTO aid_programs (name, target_localities, max_income, min_dependents, available_funds) VALUES (?, ?, ?, ?, ?)", aid_programs)

conn.commit()
conn.close()
print("Database initialized with sample data!")