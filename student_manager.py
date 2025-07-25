from database import Database

class StudentManager:
    def __init__(self, db: Database):
        self.db = db

    def add_student(self):
        print("\n--- Add New Student ---")
        name = input("Enter student name: ")
        contact = input("Enter student contact info (phone/email): ")
        locality = input("Enter student locality: ")
        while True:
            try:
                income_level = float(input("Enter family income level: "))
                break
            except ValueError:
                print("Invalid input. Please enter a number for income level.")
        while True:
            try:
                num_dependents = int(input("Enter number of dependents: "))
                break
            except ValueError:
                print("Invalid input. Please enter an integer for number of dependents.")

        query = "INSERT INTO Students (name, contact, locality, income_level, num_dependents) VALUES (?, ?, ?, ?, ?)"
        if self.db.execute_query(query, (name, contact, locality, income_level, num_dependents)):
            print(f"Student '{name}' added successfully.")
        else:
            print(f"Failed to add student '{name}'.")

    def view_students(self, filter_by_locality=None, filter_by_status=None):
        """Displays a list of registered students, with options to filter."""
        print("\n--- View Students ---")
        query = "SELECT student_id, name, contact, locality, income_level, num_dependents FROM Students WHERE 1=1"
        params = []

        if filter_by_locality:
            query += " AND locality LIKE ?"
            params.append(f"%{filter_by_locality}%")

        if filter_by_status and filter_by_status.lower() == 'needy':
            needy_threshold = 50000  # Example: annual income below 50,000
            query += " AND income_level < ?"
            params.append(needy_threshold)

        students = self.db.fetch_all(query, params)

        if not students:
            print("No students found matching the criteria.")
            return

        print(f"{'ID':<5} {'Name':<20} {'Contact':<25} {'Locality':<15} {'Income':<10} {'Dependents':<10}")
        print("-" * 85)
        for student in students:
            print(f"{student[0]:<5} {student[1]:<20} {student[2]:<25} {student[3]:<15} {student[4]:<10.2f} {student[5]:<10}")

    def update_student_profile(self):
        """Modifies existing student information."""
        student_id_str = input("Enter the ID of the student to update: ")
        try:
            student_id = int(student_id_str)
        except ValueError:
            print("Invalid student ID. Please enter a number.")
            return

        print(f"\n--- Update Student Profile (ID: {student_id}) ---")
        student = self.db.fetch_one("SELECT * FROM Students WHERE student_id = ?", (student_id,))

        if not student:
            print(f"No student found with ID: {student_id}")
            return

        print(f"Current Name: {student[1]}")
        new_name = input("Enter new name (press Enter to keep current): ")
        if not new_name:
            new_name = student[1]

        print(f"Current Contact: {student[2]}")
        new_contact = input("Enter new contact (press Enter to keep current): ")
        if not new_contact:
            new_contact = student[2]

        print(f"Current Locality: {student[3]}")
        new_locality = input("Enter new locality (press Enter to keep current): ")
        if not new_locality:
            new_locality = student[3]

        current_income_level = student[4]
        print(f"Current Income Level: {current_income_level}")
        new_income_level_str = input("Enter new income level (press Enter to keep current): ")
        if new_income_level_str:
            try:
                new_income_level = float(new_income_level_str)
            except ValueError:
                print("Invalid input for income level. Keeping current value.")
                new_income_level = current_income_level
        else:
            new_income_level = current_income_level

        current_num_dependents = student[5]
        print(f"Current Number of Dependents: {current_num_dependents}")
        new_num_dependents_str = input("Enter new number of dependents (press Enter to keep current): ")
        if new_num_dependents_str:
            try:
                new_num_dependents = int(new_num_dependents_str)
            except ValueError:
                print("Invalid input for number of dependents. Keeping current value.")
                new_num_dependents = current_num_dependents
        else:
            new_num_dependents = current_num_dependents

        query = "UPDATE Students SET name=?, contact=?, locality=?, income_level=?, num_dependents=? WHERE student_id=?"
        params = (new_name, new_contact, new_locality, new_income_level, new_num_dependents, student_id)
        if self.db.execute_query(query, params):
            print(f"Student ID {student_id} updated successfully.")
        else:
            print(f"Failed to update student ID {student_id}.")

    def delete_student(self):
        """Removes a student record from the system."""
        student_id_str = input("Enter the ID of the student to delete: ")
        try:
            student_id = int(student_id_str)
        except ValueError:
            print("Invalid student ID. Please enter a number.")
            return

        print(f"\n--- Delete Student (ID: {student_id}) ---")
        confirm = input(f"Are you sure you want to delete student ID {student_id} and all associated aid allocations? (yes/no): ").lower()
        if confirm == 'yes':
            query = "DELETE FROM Students WHERE student_id = ?"
            if self.db.execute_query(query, (student_id,)):
                if self.db.cursor.rowcount > 0: # Check if a row was actually deleted
                    print(f"Student ID {student_id} and associated aid allocations deleted successfully.")
                else:
                    print(f"No student found with ID: {student_id}")
            else:
<<<<<<< HEAD
                print(f"No student found with ID {student_id}😔.")
        except mysql.connector.Error as e:
            print(f"Error retrieving student: {e}")

    # Method to filter a student
    def filter_students(self, filter_by_region=None, filter_by_status=None):
        query3 = "SELECT * FROM Students"
        conditions = []
        values = []

        if filter_by_region:
            conditions.append("region = %s")
            values.append(filter_by_region)

        if filter_by_status:
            conditions.append("aid_status = %s")
            values.append(filter_by_status)

        if conditions:
            query3 += " WHERE " + " AND ".join(conditions)

        self.cursor.execute(query3, values)
        results = self.cursor.fetchall()

        for row in results:
            print(row)

    # Method to Update Student Information
    def update_student_info(self, student_id, field, new_value):
        try:
            if field not in ['name', 'contact', 'dob', 'school', 'region', 'income', 'dependents', 'aid_status']:
                print("Invalid field name.")
                return
            query = f"UPDATE Students SET {field} = %s WHERE id = %s"
            self.cursor.execute(query, (new_value, student_id))
            self.connection.commit()
            print(" Student info updated successfully.")
        except mysql.connector.Error as e:
            print(f"Error updating student info: {e}")
    # Method to update the student profile details
    def update_student(self, student_id, updates : dict):
        """
        This defines the property to update student details in updates dict.
        
        Args:
        student_id(INT): The ID of the student to update.
        updates (dict): A dictionary of field names and their new values.
                        e.g, {'name': 'Jane Doe', 'income': 30000}
        """
        if not updates:
            print("No updates provided.")
            return 
        
        # Creating a SET clause which is dynamic through Looking over dictionary of fields which can be updated
        set_clause = ", ".join([f"{field} = %s" for field in updates.keys()])
        values = list(updates.values())
        values.append(student_id)


        #Join the update strings into one SQL statement
        query1 = f"UPDATE Students SET {set_clause} WHERE id = %s"

        # Executing the query and committing the updates
        try:
            self.cursor.excute(query1, values)
            self.connection.commit()
            print(f"Student {student_id} updated successfully.")
        except Exception as e:
            print(f"Error updating student: {e}")

    # Method to list all students
    def list_all_students(self):
        try:
            self.cursor.execute("SELECT * FROM Students")
            students = self.cursor.fetchall()
            if students:
                print("\n--- All Students ---")
                for student in students:
                    print(student)
            else:
                print("No student records found.")
        except mysql.connector.Error as e:
            print(f"Error retrieving students: {e}")

    # Method to delete the student record
    def delete_student(self, student_id):
        query2 = "DELETE FROM Students WHERE id = %s"
        self.cursor.execute(query2, (student_id,))
        self.connection.commit()
        print("Student deleted successfully.")

def prompt_and_add_student():
    print("Welcome, we are creating a profile for you...")
    name = input("Please may you enter your full name: ")
    contact = input("Enter your contact number: ")
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    income = float(input("Please you enter the average income in your household monthly (RWF) ending with .00: "))
    dependents = int(input("Enter number of dependents in your household "
    "(don't worry it means the number of people who depend on that income): "))
    region = input("Enter your region: ")
    school = input("Enter your school: ")
    manager = StudentManager()

    student = Student(None, name, contact, dob, income, dependents, region, school)

    manager.add_student(student)

if __name__ == "__main__":
    manager = StudentManager()

    # List all students
    print("\n Testing: List All Students")
    manager.list_all_students()

    # View one student by ID
    print("\n Testing: View Student Details")
    manager.view_student_details(1)  # Use a valid ID from your DB

    # Update student info
    print("\n Testing: Update Student Info")
    manager.update_student_info(1, "contact", "0788888888")  # Use a valid ID and field

=======
                print(f"Failed to delete student ID {student_id}.")
        else:
            print("Student deletion cancelled.")
>>>>>>> 9fe838b501c6e3897da97dd2f26012b58d75de44
