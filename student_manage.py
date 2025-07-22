from db_connection import create_connection


def add_student():
    dbconn = create_connection()
    cursor = dbconn.cursor()

    name = input("Enter student name: ")
    school = input("Enter school name: ")
    income = float(input("Enter househol income: "))
    dependants = int(input("Enter number of dependents: "))
    region = input("Enter region/locality: ")
    print("Information inserted successfully")


add_student()
