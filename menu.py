from student_manager import *
from student import Student

def display_main_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("         STUDENT AID MANAGEMENT SYSTEM")
    print("="*50)
    print("Welcome to the Student Aid Management system")
    print("1. Student Management")
    print("2. Aid Program Management") 
    print("3. Reports & Analytics")
    print("4. Exit")
    print("-"*50)

def display_student_menu():
    """Display the student management sub-menu."""
    print("\n" + "="*40)
    print("       STUDENT MANAGEMENT")
    print("="*40)
    print("Welcome to the Student Management section")
    print("1. Add New Student")
    print("2. View Student Details")
    print("3. Update Student Information")
    print("4. List All Students")
    print("5. Back to Main Menu")
    print("-"*40)

def display_aid_menu():
    """Display the aid program management sub-menu."""
    print("\n" + "="*40)
    print("    AID PROGRAM MANAGEMENT")
    print("="*40)
    print("Welcome to the Aid Program Management section")
    print("1. Create New Aid Program")
    print("2. Assign Aid to Student")
    print("3. Back to Main Menu")
    print("-"*40)

def get_user_choice(menu_type="main"):
    """
    Handle user input for menu selections with validation.
    
    Args:
        menu_type (str): Type of menu ("main", "student", "aid")
        
    Returns:
        int: Valid menu choice selected by user
    """
    # Define valid choices for each menu type
    valid_choices = {
        "main": [1, 2, 3, 4],
        "student": [1, 2, 3, 4, 5],
        "aid": [1, 2, 3]
    }
    
    while True:
        try:
            choice = input(f"Please enter your choice: ").strip()
            
            # Handle empty input
            if not choice:
                print("Error: Please enter a valid option.")
                continue
                
            # Convert to integer
            choice = int(choice)
            
            # Validate choice based on menu type
            if choice in valid_choices.get(menu_type, []):
                return choice
            else:
                print(f"Error: Please enter a number between {min(valid_choices[menu_type])} and {max(valid_choices[menu_type])}.")
                
        except ValueError:
            print("Error: Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return None

def demo_navigation():
    """Demonstration of the menu navigation system."""
    print("Menu Navigation System Demo")
    
    while True:
        display_main_menu()
        # choice = get_user_choice("main")
        choice = get_user_choice("main")
        
        if choice is None:  # User pressed Ctrl+C
            break
            
        if choice == 1:
            while True:
                display_student_menu()
                student_choice = get_user_choice("student")
                
                if student_choice is None:
                    break
                elif student_choice == 5:  # Back to main menu
                    break
                elif student_choice == 1: #Add New student
                    prompt_and_add_student()
                    input("Student added. Press Enter to continue...")
                else:
                    print(f"You selected student option {student_choice}")
                    input("Press Enter to continue...")
                    
        elif choice == 2:
            while True:
                display_aid_menu()
                aid_choice = get_user_choice("aid")
                
                if aid_choice is None:
                    break
                elif aid_choice == 9:  # Back to main menu
                    break
                else:
                    print(f"You selected aid program option {aid_choice}")
                    input("Press Enter to continue...")
                    
        elif choice == 3:
            print("Reports & Analytics - Feature coming soon!")
            input("Press Enter to continue...")
            
        elif choice == 5:
            print("Thank you for using the Student Aid Management System!")
            break

# Example usage
if __name__ == "__main__":
    demo_navigation()