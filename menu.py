class Menu:
    def display_main_menu(self):
        """Presents the top-level options."""
        cyan = "\033[96m"
        bold = "\033[1m"
        reset = "\033[0m"

        print(cyan + bold)
        print("+=======================================================+")
        print("||                                                     ||")
        print("||      Welcome to the Student Aid Management System   ||")
        print("||                                                     ||")
        print("||       🗃️ Track Students  | 💸 Manage Aid Programs    ||")
        print("||                                                     ||")
        print("+=======================================================+")
        print(reset)
        
        print("\n===== Financial Aid Management System =====")
        print("1. Student Management")
        print("2. Financial Aid Program Management")
        print("3. Matching and Allocation")
        print("4. Reporting and Analytics")
        print("5. Exit")
        print("===========================================")

    def display_student_menu(self):
        """Sub-menu for student-related tasks."""
        print("\n--- Student Management ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student Profile")
        print("4. Delete Student")
        print("5. Back to Main Menu")
        print("--------------------------")

    def display_subchoice(self):
        """Sub-menu for student-related tasks."""
        print("\n--- View Students ---")
        print("1. View All Students")
        print("2. Filter Students")
        print("3. Back to Student Menu")
        

    def display_aid_menu(self):
        """Sub-menu for aid program management."""
        print("\n--- Financial Aid Program Management ---")
        print("1. Add Aid Program")
        print("2. View Aid Programs")
        print("3. Update Aid Program")
        print("4. Delete Aid Program")
        print("5. Back to Main Menu")
        print("----------------------------------------")

    def display_allocation_menu(self):
        """Sub-menu for matching and allocation tasks."""
        print("\n--- Matching and Allocation ---")
        print("1. Match Students to Aid / Find Eligible Students")
        print("2. Allocate Aid")
        print("3. Allocate By Priority")
        print("4. Back to Main Menu")
        print("------------------------------")

    def display_report_menu(self):
        """Sub-menu for reporting and analytics tasks."""
        print("\n--- Reporting and Analytics ---")
        print("1. Generate Aid Report")
        # print("2. Generate Needy Student List")
        print("3. Back to Main Menu")
        print("-------------------------------")

    def get_user_choice(self, prompt="Enter your choice: "):
        """Handles user input for menu selections."""
        return input(prompt).strip()