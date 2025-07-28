from db_connect import connect_to_database

conn = connect_to_database()
def allocate_by_priority():
    """New priority-based allocation method using existing priority_index"""
    program_id = input("Program ID: ")
    
    if not program_id.isdigit():
        print("Invalid Program ID")
        return
    
    cursor = conn.cursor()
    
    # Check if program exists and get available funds
    cursor.execute("SELECT * FROM AidPrograms WHERE id = %s", (program_id,))
    program = cursor.fetchone()
    
    if not program:
        print("Program not found")
        return
    
    available_funds = program[4]
    print(f"Program: {program[1]}")
    print(f"Available funds: {available_funds} RWF")
    
    # Get all eligible students with their priority_index
    try:
        cursor.execute("""
            SELECT s.id, s.name, s.income, s.dependents, s.amount_needed, s.priority_index
            FROM Students s
            LEFT JOIN allocations a ON s.id = a.student_id 
                AND a.program_id = %s AND a.status = 'Successful'
            WHERE s.amount_needed > 0 
            AND s.priority_index IS NOT NULL
            AND a.student_id IS NULL
            ORDER BY s.priority_index DESC
        """, (program_id,))
    except:
        # If allocations table doesn't exist, get all eligible students
        cursor.execute("""
            SELECT id, name, income, dependents, amount_needed, priority_index
            FROM Students 
            WHERE amount_needed > 0 
            AND priority_index IS NOT NULL
            ORDER BY priority_index DESC
        """)
    
    
    students = cursor.fetchall()
    
    if not students:
        print("No eligible students found")
        return
    
    # Students are already sorted by priority_index (highest first)
    student_priorities = []
    for student in students:
        student_id, name, income, dependents, amount_needed, priority_index = student
        student_priorities.append((student_id, name, income, dependents, amount_needed, priority_index))
    
    # Display top candidates
    print(f"\nTop {min(10, len(student_priorities))} priority students:")
    print("-" * 80)
    print(f"{'Rank':<4} {'Name':<15} {'Income':<10} {'Deps':<5} {'Need':<10} {'Priority':<8}")
    print("-" * 80)
    
    for i, (student_id, name, income, deps, need, priority_index) in enumerate(student_priorities[:10]):
        print(f"{i+1:<4} {name:<15} {income:<10} {deps:<5} {need:<10} {priority_index:<8}")
    
    # Allocation options
    print("\nAllocation options:")
    print("1. Allocate to highest priority student")
    # print("2. Allocate to top N students")
    # print("3. Allocate specific amount to a student")
    # print("4. Auto-allocate to fill as many students as possible")
    
    choice = input("Choose option (1-4): ")
    
    if choice == "1":
        # Allocate to top priority student
        top_student = student_priorities[0]
        student_id, name, income, deps, amount_needed, priority_index = top_student
        amount = min(amount_needed, available_funds)
        process_allocation(student_id, program_id, amount)
        
    elif choice == "2":
        # Allocate to top N students
        n = int(input("How many top students: "))
        remaining_funds = available_funds
        
        for i in range(min(n, len(student_priorities))):
            if remaining_funds <= 0:
                break
                
            student_id, name, income, deps, amount_needed, priority_index = student_priorities[i]
            amount = min(amount_needed, remaining_funds)
            
            if amount > 0:
                process_allocation(student_id, program_id, amount)
                remaining_funds -= amount
                print(f"Allocated {amount} RWF to {name} (Priority: {priority_index})")
    
    elif choice == "3":
        # Manual amount allocation
        rank = int(input("Enter student rank from list above: ")) - 1
        if 0 <= rank < len(student_priorities):
            student_id = student_priorities[rank][0]
            amount = float(input("Amount to allocate: "))
            process_allocation(student_id, program_id, amount)
        else:
            print("Invalid rank")
    
    elif choice == "4":
        # Auto-allocate to maximize students helped
        remaining_funds = available_funds
        allocated_count = 0
        
        for student_id, name, income, deps, amount_needed, priority_index in student_priorities:
            if remaining_funds <= 0:
                break
                
            # Allocate either full need or remaining funds, whichever is smaller
            amount = min(amount_needed, remaining_funds)
            
            if amount >= 1000:  # Minimum allocation threshold
                process_allocation(student_id, program_id, amount)
                remaining_funds -= amount
                allocated_count += 1
                print(f"Allocated {amount} RWF to {name} (Priority: {priority_index})")
        
        print(f"\nTotal students helped: {allocated_count}")
        print(f"Remaining funds: {remaining_funds} RWF")

def process_allocation(student_id, program_id, amount):
    """Process the actual allocation (common logic)"""
    cursor = conn.cursor()
    
    # Get student and program info
    cursor.execute("SELECT * FROM Students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.execute("SELECT * FROM AidPrograms WHERE id = %s", (program_id,))
    program = cursor.fetchone()
    
    if not student or not program:
        print("Student or program not found")
        return False
    
    # Check available funds
    if amount > program[4]:
        print(f"Insufficient funds. Only {program[4]} RWF available")
        return False
    
    # Record allocation
    create_allocations_table()
    sql = '''INSERT INTO allocations(student_id, program_id, amount, status)
             VALUES(%s, %s, %s, %s)'''
    cursor.execute(sql, (student_id, program_id, amount, 'Successful'))
    
    # Update available amount
    new_available = int(program[4]) - int(amount)
    cursor.execute("UPDATE AidPrograms SET available_funds = %s WHERE id = %s",
                   (new_available, program_id))
    
    conn.commit()
    print(f"Successfully allocated {amount} RWF from {program[1]} to {student[1]}")
    return True

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