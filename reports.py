from db_connect import connect_to_database

conn = connect_to_database()

cursor = conn.cursor()

    

    # def generate_aid_report(self, locality=None):
        
    #     print("\n--- Aid Allocation Report ---")
    #     query_allocated_aid = """
    #         SELECT SUM(aa.amount), COUNT(DISTINCT aa.student_id)
    #         FROM AidAllocations aa
    #         JOIN Students s ON aa.student_id = s.student_id
    #         WHERE 1=1
    #     """
    #     query_remaining_funds = """
    #         SELECT ap.name, ap.available_funds, ap.target_localities
    #         FROM AidPrograms ap
    #         WHERE 1=1
    #     """
    #     params = []

    #     if locality:
    #         query_allocated_aid += " AND s.locality LIKE ?"
    #         query_remaining_funds += " AND ap.target_localities LIKE ?"
    #         params.append(f"%{locality}%")

    #     # Total Aid Allocated & Students Supported
    #     result_allocated = self.db.fetch_one(query_allocated_aid, params)
    #     total_allocated = result_allocated[0] if result_allocated[0] else 0
    #     students_supported = result_allocated[1] if result_allocated[1] else 0

    #     print(f"Total Aid Allocated: {total_allocated:.2f}")
    #     print(f"Total Unique Students Supported: {students_supported}")

    #     print("\nRemaining Aid Funds by Program:")
    #     remaining_funds_programs = self.db.fetch_all(query_remaining_funds, params)
    #     if remaining_funds_programs:
    #         print(f"{'Program Name':<30} {'Available Funds':<18} {'Target Localities':<25}")
    #         print("-" * 73)
    #         for program in remaining_funds_programs:
    #             print(f"{program[0]:<30} {program[1]:<18.2f} {program[2]:<25}")
    #     else:
    #         print("No aid programs found matching the locality criteria or no remaining funds.")

def generate_aid_report():
    """Simple display of all allocation data"""
    print("\n--- Aid Allocation Report ---")
    
    try:
            # Get all allocations with student and program details
        query = """
                SELECT 
                    aa.id,
                    s.name as student_name,
                    ap.name as program_name,
                    aa.amount,
                    aa.status,
                    aa.created_at
                FROM allocations aa
                JOIN Students s ON aa.student_id = s.id
                JOIN AidPrograms ap ON aa.program_id = ap.id
                ORDER BY aa.created_at DESC
            """
        cursor.execute(query)
        allocations = cursor.fetchall()
            
        if allocations:
                # Display header
            print(f"{'ID':<5} {'Student Name':<25} {'Program':<20} {'Amount':<12} {'Status':<10} {'Date':<12}")
            print("-" * 84)
                
                # Display each allocation
            total_amount = 0
            for allocation in allocations:
                allocation_id = allocation[0]
                student_name = allocation[1][:24] if allocation[1] else "Unknown"
                program_name = allocation[2][:19] if allocation[2] else "Unknown"
                amount = float(allocation[3]) if allocation[3] else 0
                status = allocation[4] or "Unknown"
                date = str(allocation[5])[:10] if allocation[5] else "Unknown"
                    
                print(f"{allocation_id:<5} {student_name:<25} {program_name:<20} ${amount:<11.2f} {status:<10} {date}")
                total_amount += amount
                
                # Display summary
                print("-" * 84)
                print(f"Total Allocations: {len(allocations)}")
                print(f"Total Amount: RWF{total_amount:,.2f}")
                
        else:
            print("No allocations found.")
                
    except Exception as e:
            print(f"Error generating report: {e}")
            print("Please check your database connection and table names.")
   
    # def generate_needy_student_list(self, locality=None):
    #     """Creates a report of identified needy students."""
    #     print("\n--- Needy Student List ---")
    #     # Define 'needy' based on your criteria (e.g., income below a threshold)
    #     needy_threshold = 50000 # Example threshold

    #     query = "SELECT student_id, name, contact, locality, income_level, num_dependents FROM Students WHERE income_level < ?"
    #     params = [needy_threshold]

    #     if locality:
    #         query += " AND locality LIKE ?"
    #         params.append(f"%{locality}%")

    #     query += " ORDER BY income_level ASC" # Show neediest first

    #     needy_students = self.db.fetch_all(query, params)

    #     if not needy_students:
    #         print("No needy students found matching the criteria.")
    #         return

    #     print(f"Criteria for 'Needy': Family Income Below {needy_threshold:.2f}")
    #     print(f"{'ID':<5} {'Name':<20} {'Contact':<25} {'Locality':<15} {'Income':<10} {'Dependents':<10}")
    #     print("-" * 85)
    #     for student in needy_students:
    #         print(f"{student[0]:<5} {student[1]:<20} {student[2]:<25} {student[3]:<15} {student[4]:<10.2f} {student[5]:<10}")