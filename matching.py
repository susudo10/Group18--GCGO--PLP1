# File: matching.py
def match_students_to_aid(conn):
    """Match students to suitable aid programs"""
    print("\n--- Match Students to Aid ---")
    
    # Get student ID
    student_id = input("Enter student ID (or leave blank to match by criteria): ")
    if student_id:
        if not student_id.isdigit():
            print("Invalid ID")
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        
        if not student:
            print("Student not found")
            return
        
        # Find programs matching student's region and need level
        cursor.execute('''SELECT * FROM aid_programs 
                          WHERE region = ? AND available_amount > 0''', 
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
                      WHERE region = ? AND need_level = ?''', 
                  (region, need_level))
    students = cursor.fetchall()
    
    if not students:
        print("No students match the criteria")
        return
    
    print("\nStudents matching criteria:")
    for student in students:
        print(f"ID: {student[0]}, Name: {student[1]}, Income: {student[6]} RWF")
    
    cursor.execute('''SELECT * FROM aid_programs 
                      WHERE region = ? AND available_amount > 0''', 
                  (region,))
    programs = cursor.fetchall()
    
    if not programs:
        print("No aid programs available in this region")
        return
    
    print("\nAvailable aid programs:")
    for program in programs:
        print(f"ID: {program[0]}, Name: {program[1]}, Available: {program[5]} RWF")

def allocate_aid(conn):
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
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    cursor.execute("SELECT * FROM aid_programs WHERE id = ?", (program_id,))
    program = cursor.fetchone()
    
    if not student or not program:
        print("Student or program not found")
        return
    
    # Check available funds
    if amount > program[5]:
        print(f"Insufficient funds. Only {program[5]} RWF available")
        return
    
    # Record allocation
    sql = ''' INSERT INTO allocations(student_id, program_id, amount, status)
              VALUES(?,?,?,?) '''
    cursor.execute(sql, (student_id, program_id, amount, 'Pending'))
    
    # Update available amount
    new_available = program[5] - amount
    cursor.execute("UPDATE aid_programs SET available_amount = ? WHERE id = ?", 
                  (new_available, program_id))
    
    conn.commit()
    print(f"Allocated {amount} RWF from {program[1]} to {student[1]}")