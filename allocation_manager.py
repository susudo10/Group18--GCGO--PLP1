# from database import Database
from db_connect import connect_to_database

conn = connect_to_database()
def match_students_to_aid():
    """Match students to suitable aid programs"""
    print("\n--- Match Students to Aid ---")
    
    # Get student ID
    student_id = int(input("Enter student ID (or leave blank to match by criteria): "))
    if student_id:
        # if not student_id.isdigit():
        #     print("Invalid ID")
        #     return
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        
        if not student:
            print("Student not found")
            return
        
        # Find programs matching student's region and need level
        cursor.execute('''SELECT * FROM AidPrograms 
                          WHERE target_locality = %s AND available_funds > 0''', 
                      (student[5],))
        programs = cursor.fetchall()
        
        if not programs:
            print("No suitable aid programs found for this student")
            return
        
        print(f"\nSuitable aid programs for {student[1]}:")
        for program in programs:
            print(f"ID: {program[0]}, Name: {program[1]}, Available: {program[5]} RWF")
        
        return
    
    # If no student ID provided, match by criteria
    region = input("Region: ")
    need_level = input("Need Level (Low/Medium/High): ").capitalize()
    
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM students 
                      WHERE region =  %s AND need_level =  %s''', 
                  (region, need_level))
    students = cursor.fetchall()
    
    if not students:
        print("No students match the criteria")
        return
    
    print("\nStudents matching criteria:")
    for student in students:
        print(f"ID: {student[0]}, Name: {student[1]}, Income: {student[6]} RWF")
    
    cursor.execute('''SELECT * FROM AidPrograms 
                      WHERE region =  %s AND available_funds > 0''', 
                  (region,))
    programs = cursor.fetchall()
    
    if not programs:
        print("No aid programs available in this region")
        return
    
    print("\nAvailable aid programs:")
    for program in programs:
        print(f"ID: {program[0]}, Name: {program[1]}, Available: {program[5]} RWF")

def allocate_aid():
    """Allocate aid to a student"""
    print("\n--- Allocate Aid to Student ---")
    student_id = input("Student ID: ")
    program_id = input("Program ID: ")
    amount = float(input("Amount to allocate (RWF): "))
    
    if not student_id.isdigit() or not program_id.isdigit():
        print("Invalid ID")
        return
    
    # Check student and program exist
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students WHERE id =  %s", (student_id,))
    student = cursor.fetchone()
    cursor.execute("SELECT * FROM AidPrograms WHERE id =  %s", (program_id,))
    program = cursor.fetchone()
    
    if not student or not program:
        print("Student or program not found")
        return
    
    # Check available funds
    if amount > program[4]:
        print(f"Insufficient funds. Only {program[4]} RWF available")
        return
    
    # Record allocation
    create_allocations_table()
    sql = ''' INSERT INTO allocations(student_id, program_id, amount, status)
              VALUES(%s, %s, %s, %s) '''
    cursor.execute(sql, (student_id, program_id, amount, 'Successful'))
    
    # Update available amount
    new_available = int(program[4]) - int(amount)
    cursor.execute("UPDATE AidPrograms SET available_funds =  %s WHERE id =  %s", 
                  (new_available, program_id))
    
    conn.commit()
    print(f"Allocated {amount} RWF from {program[1]} to {student[1]}")

def create_allocations_table():
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS allocations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    program_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (program_id) REFERENCES AidPrograms(id)
    )
'''
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    print("Allocations table created successfully")