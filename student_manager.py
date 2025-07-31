#!/usr/bin/python3
"""
Manages student records with database operations and user prompts.
"""

import mysql.connector
from student import Student  # Assuming you have a Student class in student.py
import os
from dotenv import load_dotenv
from db_connection import create_connection
load_dotenv()


class StudentManager:
    def __init__(self, db):
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )
        self.cursor = self.connection.cursor()

    def add_student(self, student: Student):
        try:
            self.cursor.execute(
                """
                INSERT INTO Students (name, contact, dob, income, dependents, region, school, amount_needed, priority_index) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    student.name,
                    student.contact,
                    student.dob,
                    student.income,
                    student.dependents,
                    student.region,
                    student.school,
                    student.amount_needed,
                    student.priority_index
                )
            )
            self.connection.commit()
            print(f"\n✅ Student '{student.name}' added successfully.✅")

        except mysql.connector.Error as e:
            print(f"❌ Error adding student: {e}")
    
    def view_student_details(self, student_id):
        try:
            self.cursor.execute("SELECT id, name, contact, dob, income, dependents, region, school, aid_status FROM Students WHERE id = %s", (student_id,))
            student = self.cursor.fetchone()

            if not student:
                print(f"No student found with ID {student_id}.")
                return

            print("\n--- Student Profile ---")
            print("-" * 40)
            print(f"{'ID':<15}: {student[0]}")
            print(f"{'Full Name':<15}: {student[1]}")
            print(f"{'Contact':<15}: {student[2]}")
            print(f"{'Date of Birth':<15}: {student[3]}")
            print(f"{'Income (RWF)':<15}: {student[4]:,.2f}")
            print(f"{'Dependents':<15}: {student[5]}")
            print(f"{'Amount needed':<15}: {student[5]}")
            print(f"{'Region':<15}: {student[6]}")
            print(f"{'School':<15}: {student[7]}")
            print(f"{'Aid Status':<15}: {student[8] or 'N/A'}")
            print("-" * 40)

        except mysql.connector.Error as e:
            print(f"Error retrieving student details: {e}")

    def filter_students(self, region=None, aid_status=None):
        query = "SELECT * FROM Students WHERE 1=1"
        params = []
        if region:
            query += " AND region = %s"
            params.append(region)
        if aid_status:
            query += " AND aid_status = %s"
            params.append(aid_status)

        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        if not results:
            print("No students found matching the criteria.")
            return
        
        headers = [desc[0] for desc in self.cursor.description]
        print(" | ".join(f"{h:<15}" for h in headers))
        print("-" * (len(headers)*18))
        for row in results:
            print(" | ".join(f"{str(field):<15}" for field in row))


    def list_all_students(self):
        self.cursor.execute("SELECT * FROM Students")
        students = self.cursor.fetchall()
        if not students:
            print("No student records found.")
            return
    
        # Print header row 
<<<<<<< HEAD
        print(f"{'ID':<4} {'Name':<20} {'Contact':<12} {'DOB':<12} {'School':<10} {'Region':<5} {'Income':<10} {'Dependents':<15} {'Priority Index':<10}")
=======
        print(f"{'ID':<4} {'Name':<20} {'Contact':<12} {'DOB':<12} {'School':<10} {'Region':<5} {'Income':<10} {'Dependents':<15} {'Aid Status':<10}")
>>>>>>> ae22e82ef153d0afc5c1cdb09812eb3079e31873
        print("-" * 110)
    
        for student in students:
            income_val = student[4]
            try:
                income_val = f"{float(income_val):.2f}"
            except (TypeError, ValueError):
                income_val = str(income_val) if income_val is not None else "N/A"
        
            print(f"{student[0]:<4} {student[1]:<20} {student[2]:<12} {str(student[3]):<12} {income_val:<10} "
              f"{student[5]:<5} {student[6]:<10} {student[7]:<15} {student[10] or 'N/A':<10}")


    
    def update_student_info(self, student_id, field, new_value):
        valid_fields = ['name', 'contact', 'dob', 'school', 'region', 'income', 'dependents', 'priority_index']
        if field not in valid_fields:
            print("❌ Invalid field name.")
            return
        try:
            query = f"UPDATE Students SET {field} = %s WHERE id = %s"
            self.cursor.execute(query, (new_value, student_id))
            self.connection.commit()
            print("✅ Student info updated successfully.")
        except mysql.connector.Error as e:
            print(f"❌ Error updating student info: {e}")

    
    def delete_student(self, student_id):
        try:
            self.cursor.execute("DELETE FROM Students WHERE id = %s", (student_id,))
            self.connection.commit()
            print(f"🗑️ Student with ID {student_id} deleted successfully.")
        except mysql.connector.Error as e:
            print(f"❌ Error deleting student: {e}")

def prompt_and_add_student(student_mgr):
    print("📝 Let's create a new student profile...")
    name = input("Full Name: ")
    contact = input("Contact Number: ")
    dob = input("Date of Birth (YYYY-MM-DD): ")

    try:
        income = int(input("💰 Average Monthly Income (RWF): "))
        dependents = int(input(" Number of Dependents(Meaning number of people depending on that income): "))
        amount_needed = int(input("Enter Amount needed): "))
        pr_index = calculate_priority(income, dependents, amount_needed)
    except ValueError:
        print("❌ Invalid number format. Please try again.")
        return

    region = input("Region: ")
    school = input("School: ")

    student = Student(
        id=None,
        name=name,
        contact=contact,
        dob=dob,
        income=income,
        dependents=dependents,
        region=region,
        school=school,
        amount_needed=amount_needed,
        priority_index=pr_index
    )
<<<<<<< HEAD

    student_mgr.add_student(student)

def calculate_priority(income, dependents, amount_needed, w1=0.5, w2=0.3, w3=0.2):
    # Normalize to 0-10 scale (you can adjust max values based on your data)
    income_score = (50000 - income) / 50000 * 10  # Lower income = higher score
    dependents_score = dependents / 8 * 10        # More dependents = higher score  
    amount_score = amount_needed / 5000 * 10      # Higher amount = higher score
    
    # Calculate weighted priority index
    priority = income_score * w1 + dependents_score * w2 + amount_score * w3
    return round(priority, 2)
=======
>>>>>>> ae22e82ef153d0afc5c1cdb09812eb3079e31873
