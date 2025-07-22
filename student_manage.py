from db_connection import create_connection


# This is a function to add a student and their family details
def add_student():
    dbconn = create_connection()
    cursor = dbconn.cursor()

    name = input("Enter student name: ")
    school = input("Enter school name: ")
    dob = input("Enter your date of birth in this format DD-MM-YYY")
    income = float(input("Enter househol income: "))
    dependants = int(input("Enter number of dependents: "))
    region = input("Enter region/locality: ")
    

    # This is inserting the input from the user into the database
    cursor.execute(
    "INSERT INTO students (name, contact, income, dob, dependents, region)
    VALUES (%s, %s, %s, %s, %s, %s)", (name, contact, income, dob dependents, region))

    # Committing the insertion
    dbconn.commit()
    print("Student was added successfully. ✅")

    
    #Closing the connection
    cursor.close()
    dbconn.close()
