from database import Database

class AllocationManager:
    def __init__(self, db: Database):
        self.db = db

    def match_students_to_aid(self):
        print("\n--- Match Students to Aid / Find Eligible Students ---")
        print("1. Find aid programs for a specific student")
        print("2. Find students eligible for a specific aid program")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            student_id_str = input("Enter the student ID: ")
            try:
                student_id = int(student_id_str)
            except ValueError:
                print("Invalid student ID.")
                return

            student = self.db.fetch_one("SELECT * FROM Students WHERE student_id = ?", (student_id,))
            if not student:
                print(f"Student with ID {student_id} not found.")
                return

            s_name, s_contact, s_locality, s_income, s_dependents = student[1], student[2], student[3], student[4], student[5]
            print(f"\nMatching aid programs for student: {s_name} (ID: {student_id})")
            print(f"  Locality: {s_locality}, Income: {s_income}, Dependents: {s_dependents}")

            query = """
                SELECT aid_id, name, type, eligibility_criteria, available_funds, target_localities
                FROM AidPrograms
                WHERE target_localities LIKE ? AND available_funds > 0
            """
            potential_programs = self.db.fetch_all(query, (f"%{s_locality}%",))

            if not potential_programs:
                print("No potential aid programs found for this student based on locality and available funds.")
                return

            print("\nPotential Aid Programs (check eligibility manually):")
            print(f"{'ID':<5} {'Name':<25} {'Type':<15} {'Funds':<12} {'Eligibility Criteria'}")
            print("-" * 100)
            for prog in potential_programs:
                print(f"{prog[0]:<5} {prog[1]:<25} {prog[2]:<15} {prog[4]:<12.2f} {prog[3]}")

            print("\n(Note: Manual review of 'Eligibility Criteria' is required to confirm actual eligibility.)")

        elif choice == '2':
            aid_id_str = input("Enter the Aid Program ID: ")
            try:
                aid_id = int(aid_id_str)
            except ValueError:
                print("Invalid Aid ID.")
                return

            aid_program = self.db.fetch_one("SELECT * FROM AidPrograms WHERE aid_id = ?", (aid_id,))
            if not aid_program:
                print(f"Aid program with ID {aid_id} not found.")
                return

            p_name, p_type, p_eligibility, p_funds, p_localities = aid_program[1], aid_program[2], aid_program[3], aid_program[4], aid_program[5]
            print(f"\nFinding students eligible for aid program: {p_name} (ID: {aid_id})")
            print(f"  Type: {p_type}, Eligibility: {p_eligibility}, Funds: {p_funds}, Localities: {p_localities}")

            target_localities_list = [loc.strip() for loc in p_localities.split(',')]
            locality_placeholders = ', '.join(['?' for _ in target_localities_list])

            needy_threshold = 50000 # This threshold for the aid program eligibility criteria
            
            query = f"""
                SELECT student_id, name, contact, locality, income_level, num_dependents
                FROM Students
                WHERE locality IN ({locality_placeholders}) AND income_level < ?
            """
            
            eligible_students = self.db.fetch_all(query, target_localities_list + [needy_threshold])

            if not eligible_students:
                print("No students found eligible for this aid program based on simplified criteria.")
                return

            print("\nPotentially Eligible Students:")
            print(f"{'ID':<5} {'Name':<20} {'Contact':<25} {'Locality':<15} {'Income':<10} {'Dependents':<10}")
            print("-" * 85)
            for student in eligible_students:
                print(f"{student[0]:<5} {student[1]:<20} {student[2]:<25} {student[3]:<15} {student[4]:<10.2f} {student[5]:<10}")
            print("\n(Note: Manual review against full eligibility criteria is crucial.)")

        else:
            print("Invalid choice.")

    def allocate_aid(self):
        print("\n--- Allocate Aid ---")
        student_id_str = input("Enter Student ID for allocation: ")
        aid_id_str = input("Enter Aid Program ID for allocation: ")
        amount_str = input("Enter allocation amount: ")

        try:
            student_id = int(student_id_str)
            aid_id = int(aid_id_str)
            amount = float(amount_str)
            if amount <= 0:
                print("Allocation amount must be positive.")
                return
        except ValueError:
            print("Invalid input. Please enter numbers for IDs and amount.")
            return

        # Check if student exists
        student_exists = self.db.fetch_one("SELECT 1 FROM Students WHERE student_id = ?", (student_id,))
        if not student_exists:
            print(f"Student with ID {student_id} does not exist.")
            return

        # Check if aid program exists and has sufficient funds
        aid_program = self.db.fetch_one("SELECT available_funds FROM AidPrograms WHERE aid_id = ?", (aid_id,))
        if not aid_program:
            print(f"Aid program with ID {aid_id} does not exist.")
            return

        available_funds = aid_program[0]
        if available_funds < amount:
            print(f"Insufficient funds. Available: {available_funds:.2f}, Requested: {amount:.2f}")
            return

        # Record allocation
        query_allocation = "INSERT INTO AidAllocations (student_id, aid_id, amount) VALUES (?, ?, ?)"
        if self.db.execute_query(query_allocation, (student_id, aid_id, amount)):
            # Deduct funds from aid program
            new_funds = available_funds - amount
            query_update_funds = "UPDATE AidPrograms SET available_funds = ? WHERE aid_id = ?"
            if self.db.execute_query(query_update_funds, (new_funds, aid_id)):
                print(f"Aid of {amount:.2f} allocated to Student ID {student_id} from Aid Program ID {aid_id} successfully.")
            else:
                print("Error updating aid program funds after allocation.")
        else:
            print("Failed to record aid allocation.")