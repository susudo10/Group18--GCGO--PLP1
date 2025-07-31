from database import Database
from db_connect import connect_to_database
import mysql.connector

conn = connect_to_database()

class AidManager:
    def __init__(self, db: Database):
        self.db = db
        self.cursor = conn.cursor()
    def new_aid(self):
        name = input("Enter scholarship/program name: ")
        aid_type = input("Enter type of aid (e.g., Scholarship, Grant, Loan): ")
        eligibility_criteria = input("Enter eligibility criteria: ")
        available_funds = float(input("Enter available funds: "))
        target_localities = input("Enter target localities (comma-separated, e.g., Kigali,Gasabo): ")
        try:
            self.cursor.execute(
                """
                INSERT INTO AidPrograms (name, type, eligibility_criteria, available_funds, target_locality) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    name,
                    aid_type,
                    eligibility_criteria,
                    available_funds,
                    target_localities,
                )
            )
            conn.commit()
            print(f"\n✅ Program Aid '{name}' added successfully.✅")

        except mysql.connector.Error as e:
            print(f"❌ Error adding student: {e}")

    def add_aid_program(self):
        print("\n--- Add New Aid Program ---")
        name = input("Enter scholarship/program name: ")
        aid_type = input("Enter type of aid (e.g., Scholarship, Grant, Loan): ")
        eligibility_criteria = input("Enter eligibility criteria: ")
        while True:
            try:
                available_funds = float(input("Enter available funds: "))
                break
            except ValueError:
                print("Invalid input. Please enter a number for available funds.")
        target_localities = input("Enter target localities (comma-separated, e.g., Kigali,Gasabo): ")

        query = "INSERT INTO AidPrograms (name, type, eligibility_criteria, available_funds, target_localities) VALUES (?, ?, ?, ?, ?)"
        if self.cursor.execute(query, (name, aid_type, eligibility_criteria, available_funds, target_localities)):
            print(f"Aid program '{name}' added successfully.")
        else:
            print(f"Failed to add aid program '{name}'.")

    def view_aid_programs(self, filter_by_locality=None):
        print("\n--- View Aid Programs ---")
        query = "SELECT aid_id, name, type, eligibility_criteria, available_funds, target_localities FROM AidPrograms WHERE 1=1"
        params = []

        if filter_by_locality:
            query += " AND target_localities LIKE ?"
            params.append(f"%{filter_by_locality}%")

        aid_programs = self.db.fetch_all(query, params)

        if not aid_programs:
            print("No aid programs found matching the criteria.")
            return

        print(f"{'ID':<5} {'Name':<25} {'Type':<15} {'Funds':<12} {'Localities':<20}")
        print("-" * 80)
        for program in aid_programs:
            print(f"{program[0]:<5} {program[1]:<25} {program[2]:<15} {program[4]:<12.2f} {program[5]:<20}")

    def update_aid_program(self):
        aid_id_str = input("Enter the ID of the aid program to update: ")
        try:
            aid_id = int(aid_id_str)
        except ValueError:
            print("Invalid aid ID. Please enter a number.")
            return

        print(f"\n--- Update Aid Program (ID: {aid_id}) ---")
        program = self.db.fetch_one("SELECT * FROM AidPrograms WHERE aid_id = ?", (aid_id,))

        if not program:
            print(f"No aid program found with ID: {aid_id}")
            return

        print(f"Current Name: {program[1]}")
        new_name = input("Enter new name (press Enter to keep current): ")
        if not new_name:
            new_name = program[1]

        print(f"Current Type: {program[2]}")
        new_type = input("Enter new type (press Enter to keep current): ")
        if not new_type:
            new_type = program[2]

        print(f"Current Eligibility: {program[3]}")
        new_eligibility = input("Enter new eligibility criteria (press Enter to keep current): ")
        if not new_eligibility:
            new_eligibility = program[3]

        current_funds = program[4]
        print(f"Current Available Funds: {current_funds}")
        new_funds_str = input("Enter new available funds (press Enter to keep current): ")
        if new_funds_str:
            try:
                new_funds = float(new_funds_str)
            except ValueError:
                print("Invalid input for funds. Keeping current value.")
                new_funds = current_funds
        else:
            new_funds = current_funds

        print(f"Current Target Localities: {program[5]}")
        new_localities = input("Enter new target localities (comma-separated, press Enter to keep current): ")
        if not new_localities:
            new_localities = program[5]

        query = "UPDATE AidPrograms SET name=?, type=?, eligibility_criteria=?, available_funds=?, target_localities=? WHERE aid_id=?"
        params = (new_name, new_type, new_eligibility, new_funds, new_localities, aid_id)
        if self.db.execute_query(query, params):
            print(f"Aid program ID {aid_id} updated successfully.")
        else:
            print(f"Failed to update aid program ID {aid_id}.")

    def delete_aid_program(self):
        aid_id_str = input("Enter the ID of the aid program to delete: ")
        try:
            aid_id = int(aid_id_str)
        except ValueError:
            print("Invalid aid ID. Please enter a number.")
            return

        print(f"\n--- Delete Aid Program (ID: {aid_id}) ---")
        confirm = input(f"Are you sure you want to delete aid program ID {aid_id} and all associated aid allocations? (yes/no): ").lower()
        if confirm == 'yes':
            query = "DELETE FROM AidPrograms WHERE aid_id = ?"
            if self.db.execute_query(query, (aid_id,)):
                if self.db.cursor.rowcount > 0:
                    print(f"Aid program ID {aid_id} and associated aid allocations deleted successfully.")
                else:
                    print(f"No aid program found with ID: {aid_id}")
            else:
                print(f"Failed to delete aid program ID {aid_id}.")
        else:
            print("Aid program deletion cancelled.")