import sqlite3

class Database:
    def __init__(self, db_name="financial_aid.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect_db()
        self._create_tables()

    def _connect_db(self):#Establishes a connection to the SQLite database
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            exit()

    def _create_tables(self):#Creates necessary tables if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT,
                locality TEXT,
                income_level REAL,
                num_dependents INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS AidPrograms (
                aid_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT,
                eligibility_criteria TEXT,
                available_funds REAL,
                target_localities TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS AidAllocations (
                allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                aid_id INTEGER,
                amount REAL,
                allocation_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (aid_id) REFERENCES AidPrograms(aid_id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return False

    def fetch_all(self, query, params=()):#Fetches all results
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database fetch error: {e}")
            return []

    def fetch_one(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database fetch error: {e}")
            return None

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")