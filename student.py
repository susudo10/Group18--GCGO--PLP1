# File: student.py
def add_student(conn):
    """Add a new student to the database"""
    print("\n--- Register New Student ---")
    name = input("Name: ")
    age = input("Age: ")
    school = input("School: ")
    grade = input("Grade: ")
    region = input("Region: ")
    household_income = float(input("Household Income (RWF): "))
    dependents = int(input("Number of Dependents: "))
    contact = input("Contact Information: ")
    
    # Calculate need level
    if household_income < 100000 or dependents > 5:
        need_level = "High"
    elif household_income < 300000 or dependents > 3:
        need_level = "Medium"
    else:
        need_level = "Low"
    
    sql = ''' INSERT INTO students(name, age, school, grade, region, household_income, dependents, need_level, contact)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cursor = conn.cursor()
    cursor.execute(sql, (name, age, school, grade, region, household_income, dependents, need_level, contact))
    conn.commit()
    print(f"Successfully registered {name} with {need_level} need level")

def view_students(conn, filter_by=None, value=None):
    """View students with optional filters"""
    sql = "SELECT * FROM students"
    params = ()
    
    if filter_by == "region":
        sql += " WHERE region = ?"
        params = (value,)
    elif filter_by == "need":
        sql += " WHERE need_level = ?"
        params = (value,)
    
    cursor = conn.cursor()
    cursor.execute(sql, params)
    students = cursor.fetchall()
    
    if not students:
        print("No students found")
        return
    
    print("\n--- Student List ---")
    for student in students:
        print(f"ID: {student[0]}, Name: {student[1]}, Region: {student[5]}, Need: {student[8]}")

def update_student(conn):
    """Update a student's record"""
    student_id = input("Enter student ID to update: ")
    if not student_id.isdigit():
        print("Invalid ID")
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    
    if not student:
        print("Student not found")
        return
    
    print("\n--- Update Student ---")
    print(f"Current record: {student}")
    
    # Get updated information
    name = input(f"Name ({student[1]}): ") or student[1]
    age = input(f"Age ({student[2]}): ") or student[2]
    school = input(f"School ({student[3]}): ") or student[3]
    grade = input(f"Grade ({student[4]}): ") or student[4]
    region = input(f"Region ({student[5]}): ") or student[5]
    household_income = float(input(f"Household Income ({student[6]}): ") or student[6])
    dependents = int(input(f"Dependents ({student[7]}): ") or student[7])
    contact = input(f"Contact ({student[9]}): ") or student[9]
    
    # Recalculate need level
    if household_income < 100000 or dependents > 5:
        need_level = "High"
    elif household_income < 300000 or dependents > 3:
        need_level = "Medium"
    else:
        need_level = "Low"
    
    sql = ''' UPDATE students
              SET name = ?, age = ?, school = ?, grade = ?, region = ?,
                  household_income = ?, dependents = ?, need_level = ?, contact = ?
              WHERE id = ? '''
    cursor.execute(sql, (name, age, school, grade, region, household_income, dependents, need_level, contact, student_id))
    conn.commit()
    print("Student record updated")

def delete_student(conn):
    """Delete a student record"""
    student_id = input("Enter student ID to delete: ")
    if not student_id.isdigit():
        print("Invalid ID")
        return
    
    confirm = input("Are you sure you want to delete this student? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    print("Student record deleted")