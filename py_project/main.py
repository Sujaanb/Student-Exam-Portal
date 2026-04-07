"""
Main entry point for the Student Examination Portal
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from utils import initialize_csv_files, print_header, clear_screen
from student import student_menu
from course import course_menu
from batch import batch_menu
from department import department_menu
from examination import examination_menu
from constants import ERROR_PREFIX, SUCCESS_PREFIX


def main_menu():
    """
    Display the main menu and handle navigation.
    """
    # Initialize CSV files on startup
    initialize_csv_files()
    
    while True:
        clear_screen()
        print_header("Student Examination Portal")
        print("1. Student Details")
        print("2. Course Details")
        print("3. Batch Details")
        print("4. Department Details")
        print("5. Examination Details")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        try:
            if choice == '1':
                student_menu()
            elif choice == '2':
                course_menu()
            elif choice == '3':
                batch_menu()
            elif choice == '4':
                department_menu()
            elif choice == '5':
                examination_menu()
            elif choice == '6':
                print(f"\n{SUCCESS_PREFIX}Thank you for using Student Examination Portal!")
                print("Goodbye!\n")
                break
            else:
                print(f"{ERROR_PREFIX}Invalid choice. Please enter a number between 1 and 6.")
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print(f"\n\n{ERROR_PREFIX}Application interrupted by user")
            print("Goodbye!\n")
            break
        except Exception as e:
            print(f"\n{ERROR_PREFIX}An unexpected error occurred: {str(e)}")
            print("Please try again.\n")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"{ERROR_PREFIX}Fatal error: {str(e)}")
        print("Application will now exit.")
        sys.exit(1)
