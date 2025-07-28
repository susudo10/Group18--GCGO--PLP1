from database import Database
from student_manager import *
from db_connection import *
from aid_manager import AidManager
from allocation_manager import match_students_to_aid, allocate_aid
from reports import generate_aid_report
from allocate_by_priority import allocate_by_priority


from menu import Menu
from user_exp import clear_screen

db = Database()
student_mgr = StudentManager(db)
aid_mgr = AidManager(db)
# allocation_mgr = AllocationManager(db)
# report_mgr = ReportManager()
menu = Menu()


def main():
    clear_screen()

    while True:
        menu.display_main_menu()
        main_choice = menu.get_user_choice()
        clear_screen()

        if main_choice == '1':
            while True:
                menu.display_student_menu()
                student_choice = menu.get_user_choice()
                clear_screen()
                if student_choice == '1':
                    prompt_and_add_student(student_mgr)
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif student_choice == '2':
                    menu.display_subchoice()
                    sub_choice = input("Enter your choice: ").strip()
                    clear_screen()

                    if sub_choice == '1':
                        student_mgr.list_all_students()
                        print("These are the students that we have for now.")
                        print("Don't worry if your name is not there. You may create a profile😉")
                        input("\nPress Enter to continue...")
                        clear_screen()
                    elif sub_choice == '2':
                        filter_loc = input("Filter by locality (leave empty for all): ").strip()
                        filter_status = input("Filter by status (e.g., 'needy', leave empty for all): ").strip()
                        student_mgr.filter_students(filter_loc if filter_loc else None, filter_status if filter_status else None)
                        input("\nPress Enter to continue...")
                        clear_screen()
                    elif sub_choice == '3':
                        break
                    else:
                        print("Invalid choice. Please try again.")
                        input("\nPress Enter to continue...")
                        clear_screen()
                        filter_loc = input("Filter by locality (leave empty for all): ")
                        filter_status = input("Filter by status (e.g., 'needy', leave empty for all): ")
                        student_mgr.filter_students(filter_loc if filter_loc else None, filter_status if filter_status else None)
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif student_choice == '3':
                    student_id = input("Enter the student ID to update: ")
                    field = input("Enter the field to update (name, contact, dob, school, region, income, dependents, aid_status): ")
                    new_value = input("Enter the new value: ")
                    student_mgr.update_student_info(student_id, field, new_value)
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif student_choice == '4':
                    student_id = input("Enter the student ID to delete: ")
                    student_mgr.delete_student(student_id)
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif student_choice == '5':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    input("\nPress Enter to continue...")
                    clear_screen()

        elif main_choice == '2':
            while True:
                menu.display_aid_menu()
                aid_choice = menu.get_user_choice()
                clear_screen()
                if aid_choice == '1':
                    aid_mgr.add_aid_program()
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif aid_choice == '2':
                    filter_loc = input("Filter by target locality (leave empty for all): ")
                    aid_mgr.view_aid_programs(filter_loc if filter_loc else None)
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif aid_choice == '3':
                    aid_mgr.update_aid_program()
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif aid_choice == '4':
                    aid_mgr.delete_aid_program()
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif aid_choice == '5':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    input("\nPress Enter to continue...")
                    clear_screen()

        elif main_choice == '3':
            while True:
                menu.display_allocation_menu()
                allocation_choice = menu.get_user_choice()
                clear_screen()
                if allocation_choice == '1':
                    match_students_to_aid()
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif allocation_choice == '2':
                    allocate_aid()
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif allocation_choice == '3':
                    allocate_by_priority()
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif allocation_choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    input("\nPress Enter to continue...")
                    clear_screen()

        elif main_choice == '4':
            while True:
                menu.display_report_menu()
                report_choice = menu.get_user_choice()
                clear_screen()
                if report_choice == '1':
                    report_loc = input("Generate report for locality (leave empty for all): ")
                    generate_aid_report()
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif report_choice == '2':
                    report_loc = input("Generate needy student list for locality (leave empty for all): ")
                    # report_mgr.generate_needy_student_list(report_loc if report_loc else None)
                    input("\nPress Enter to continue...")
                    clear_screen()
                elif report_choice == '3':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    input("\nPress Enter to continue...")
                    clear_screen()

        elif main_choice == '5':
            print("Exiting Financial Aid Management System. Goodbye!")
            db.close_connection()
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")
            clear_screen()

if __name__ == "__main__":
    main()