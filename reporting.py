# File: reporting.py
def generate_report(conn, report_type):
    """Generate various reports"""
    cursor = conn.cursor()
    
    if report_type == "students":
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        
        if not students:
            print("No students registered")
            return
        
        print("\n--- Student Report ---")
        for student in students:
            print(f"ID: {student[0]}, Name: {student[1]}, Region: {student[5]}, Need: {student[8]}")
        
        # Export to file
        export = input("Export to file? (y/n): ")
        if export.lower() == 'y':
            with open('student_report.txt', 'w') as f:
                f.write("Student Aid Network - Student Report\n")
                f.write("ID | Name | Region | Need Level\n")
                for student in students:
                    f.write(f"{student[0]} | {student[1]} | {student[5]} | {student[8]}\n")
                print("Report exported to student_report.txt")
    
    elif report_type == "aid":
        cursor.execute("SELECT * FROM aid_programs")
        programs = cursor.fetchall()
        
        if not programs:
            print("No aid programs available")
            return
        
        print("\n--- Aid Programs Report ---")
        for program in programs:
            print(f"ID: {program[0]}, Name: {program[1]}, Available: {program[5]} RWF")
        
        # Export to file
        export = input("Export to file? (y/n): ")
        if export.lower() == 'y':
            with open('aid_programs_report.txt', 'w') as f:
                f.write("Student Aid Network - Aid Programs Report\n")
                f.write("ID | Name | Available Amount\n")
                for program in programs:
                    f.write(f"{program[0]} | {program[1]} | {program[5]} RWF\n")
                print("Report exported to aid_programs_report.txt")
    
    elif report_type == "allocations":
        cursor.execute('''SELECT s.name, a.name, al.amount, al.status 
                          FROM allocations al
                          JOIN students s ON al.student_id = s.id
                          JOIN aid_programs a ON al.program_id = a.id''')
        allocations = cursor.fetchall()
        
        if not allocations:
            print("No allocations recorded")
            return
        
        print("\n--- Aid Allocations Report ---")
        for alloc in allocations:
            print(f"Student: {alloc[0]}, Program: {alloc[1]}, Amount: {alloc[2]} RWF, Status: {alloc[3]}")
        
        # Export to file
        export = input("Export to file? (y/n): ")
        if export.lower() == 'y':
            with open('allocations_report.txt', 'w') as f:
                f.write("Student Aid Network - Allocations Report\n")
                f.write("Student | Program | Amount | Status\n")
                for alloc in allocations:
                    f.write(f"{alloc[0]} | {alloc[1]} | {alloc[2]} RWF | {alloc[3]}\n")
                print("Report exported to allocations_report.txt")