import mysql.connector
def connect_to_database(host, user, password, database, port):
    """Connect to the MySQL database and return the connection object."""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            port = port,
            password=password,
            database=database,
            ssl_disabled=False
        )
        if conn.is_connected():
            db_infor = conn.get_server_info
            db_name = conn.database
            print(f"Connected to MySQL database {db_infor} at {database}:{db_name}")
            return conn
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_tables():
    """Create necessary tables in the database"""
    conn = connect_to_database("mysql-3b2c714f-alustudent-809e.f.aivencloud.com", "avnadmin", "AVNS_eT5JtHKtU3AQ9fsEevK", "defaultdb", "11687")
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT,
                school VARCHAR(255),
                grade VARCHAR(50),
                region VARCHAR(100),
                household_income DECIMAL(10, 2),
                dependents INT,
                need_level VARCHAR(50),
                contact VARCHAR(100)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aid_programs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                type VARCHAR(100),
                description TEXT,
                max_amount DECIMAL(10, 2),
                available_amount DECIMAL(10, 2),
                region VARCHAR(100)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS allocations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                program_id INT NOT NULL,
                amount DECIMAL(10, 2),
                status VARCHAR(50) DEFAULT 'Pending',
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (program_id) REFERENCES aid_programs(id)
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
# connect_to_database("mysql-3b2c714f-alustudent-809e.f.aivencloud.com", "avnadmin", "AVNS_eT5JtHKtU3AQ9fsEevK", "defaultdb", "11687")