# File: aid_program.py
def add_aid_program(conn):
    """Add a new aid program to the database"""
    print("\n--- Add New Aid Program ---")
    name = input("Program Name: ")
    program_type = input("Type (e.g., Scholarship, Supplies): ")
    description = input("Description: ")
    max_amount = float(input("Maximum Amount (RWF): "))
    available_amount = float(input("Available Amount (RWF): "))
    region = input("Target Region: ")
    
    sql = ''' INSERT INTO aid_programs(name, type, description, max_amount, available_amount, region)
              VALUES(?,?,?,?,?,?) '''
    cursor = conn.cursor()
    cursor.execute(sql, (name, program_type, description, max_amount, available_amount, region))
    conn.commit()
    print(f"Successfully added {name} aid program")

def view_aid_programs(conn, filter_by=None, value=None):
    """View aid programs with optional filters"""
    sql = "SELECT * FROM aid_programs"
    params = ()
    
    if filter_by == "region":
        sql += " WHERE region = ?"
        params = (value,)
    
    cursor = conn.cursor()
    cursor.execute(sql, params)
    programs = cursor.fetchall()
    
    if not programs:
        print("No aid programs found")
        return
    
    print("\n--- Aid Programs ---")
    for program in programs:
        print(f"ID: {program[0]}, Name: {program[1]}, Type: {program[2]}, Available: {program[5]} RWF")

def update_aid_program(conn):
    """Update an aid program's details"""
    program_id = input("Enter program ID to update: ")
    if not program_id.isdigit():
        print("Invalid ID")
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM aid_programs WHERE id = ?", (program_id,))
    program = cursor.fetchone()
    
    if not program:
        print("Program not found")
        return
    
    print("\n--- Update Aid Program ---")
    print(f"Current record: {program}")
    
    # Get updated information
    name = input(f"Name ({program[1]}): ") or program[1]
    program_type = input(f"Type ({program[2]}): ") or program[2]
    description = input(f"Description ({program[3]}): ") or program[3]
    max_amount = float(input(f"Max Amount ({program[4]}): ") or program[4])
    available_amount = float(input(f"Available Amount ({program[5]}): ") or program[5])
    region = input(f"Region ({program[6]}): ") or program[6]
    
    sql = ''' UPDATE aid_programs
              SET name = ?, type = ?, description = ?, max_amount = ?, 
                  available_amount = ?, region = ?
              WHERE id = ? '''
    cursor.execute(sql, (name, program_type, description, max_amount, available_amount, region, program_id))
    conn.commit()
    print("Aid program updated")