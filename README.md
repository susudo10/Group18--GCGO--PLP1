Financial Aid Management System
This program is a comprehensive system designed to manage student information, financial aid programs, and the allocation of aid. It features a command-line interface for easy interaction and uses an SQLite database for persistent data storage.

Features
The system is broken down into several key modules, each handling specific functionalities:

1. Student Management
add_student(): Gathers and records essential student details, including name, contact, locality, family income level, and number of dependents.

view_students(filter_by_locality=None, filter_by_status=None): Displays a list of registered students with options to filter by their locality or aid status (e.g., 'needy').

update_student_profile(student_id): Modifies existing student information based on their ID.

delete_student(student_id): Removes a student record from the system, along with any associated aid allocations.

2. Financial Aid Program Management
add_aid_program(): Allows input of details for available local aid programs, such as scholarship name, type of aid, eligibility criteria, available funds, and target localities.

view_aid_programs(filter_by_locality=None): Lists all registered aid programs, with filtering options by locality.

update_aid_program(aid_id): Modifies details of an existing aid program.

delete_aid_program(aid_id): Removes an aid program record and its associated allocations.

3.  Matching & Allocation

This is a lightweight Python script designed to streamline aid distribution for student support programs.It uses SQLite to store students, aid programs, allocations, and logs. You can find suitable aid for a student or find students for a program, allocate funding while updating records, and cancel an allocation to refund funds if needed. It offers functionality for:

Matching students to appropriate aid programs based on predefined criteria
Allocating funds and ensuring accurate updates across the database
Canceling allocations and automatically refunding aid as necessary
Technology Stack

Python 3.x
Built-in sqlite3 module

4. Reporting and Analytics
generate_aid_report(locality=None): Provides summaries of aid allocated, students supported, or remaining aid funds, filterable by locality.

generate_needy_student_list(locality=None): Creates a report of identified needy students based on a predefined income threshold, filterable by locality.

5. Database Interaction
Utilizes SQLite for connecting to a database, creating necessary tables (Students, AidPrograms, AidAllocations), and performing CRUD (Create, Read, Update, Delete) operations to ensure data persistence and integrity.

6. Menu Navigation
display_main_menu(): Presents the top-level options for navigating the system.

display_student_menu(): Sub-menu for student-related tasks.

display_aid_menu(): Sub-menu for aid program management.

display_allocation_menu(): Sub-menu for matching and allocation tasks.

display_report_menu(): Sub-menu for reporting and analytics tasks.

get_user_choice(): Handles user input for menu selections.

Program Structure
The system is organized into multiple Python files:

main.py: Handles the main program loop and menu navigation.

database.py: Manages all interactions with the SQLite database, including connection, table creation, and CRUD operations.

student_manager.py: Contains the logic for all student-related functionalities.

aid_manager.py: Contains the logic for all financial aid program-related functionalities.

allocation_manager.py: Handles the core matching and aid allocation processes.

report_manager.py: Generates various analytical reports.

menu.py: Defines and displays all the user menus.

How to Run
To get the Financial Aid Management System up and running:

Save all files: Ensure all the .py files are saved then run main.py script
