"""
Department Management Module for the Student Examination Portal
"""

from constants import (
    BATCH_FILE, 'Department.csv', ERROR_PREFIX, SUCCESS_PREFIX, INFO_PREFIX
)
from utils import (
    read_csv, write_csv, append_to_csv, find_row_index, search_records,
    extract_marks_from_string, calculate_average_marks,
    print_header, print_separator, confirm_action
)
from validators import validate_id, validate_name, safe_input


def create_department():
    """
    Create a new department.
    """
    print_header("Create New Department")
    
    while True:
        # Get Department ID
        dept_id = safe_input("Enter Department ID: ", validate_id, {"id_type": "Department ID"})
        
        # Check if department already exists
        rows = read_csv('Department.csv')
        existing_ids = [row[0] for row in rows[1:]]
        
        if dept_id in existing_ids:
            print(f"{ERROR_PREFIX}Department ID already exists")
            continue
        
        # Get Department Name
        dept_name = safe_input("Enter Department Name: ", validate_name)
        
        # Add department
        append_to_csv('Department.csv', [dept_id, dept_name, ''])
        
        print(f"\n{SUCCESS_PREFIX}Department created successfully!")
        
        if not confirm_action("Create another department"):
            break


def view_department_batches():
    """
    View all batches in a department.
    """
    print_header("Department Batches")
    
    dept_id = safe_input("Enter Department ID: ", validate_id, {"id_type": "Department ID"})
    
    dept_rows = read_csv('Department.csv')
    dept_found = False
    batch_ids = []
    
    for row in dept_rows[1:]:
        if row[0] == dept_id:
            dept_found = True
            batch_ids = row[2].split(':') if row[2] else []
            break
    
    if not dept_found:
        print(f"{ERROR_PREFIX}Department ID not found")
        return
    
    print(f"\n{INFO_PREFIX}Batches in Department {dept_id}:\n")
    print_separator()
    
    batch_rows = read_csv(BATCH_FILE)
    
    for batch_id in batch_ids:
        if not batch_id.strip():
            continue
        
        for row in batch_rows[1:]:
            if row[0] == batch_id:
                print(f"Batch ID:      {row[0]}")
                print(f"Batch Name:    {row[1]}")
                print_separator()
                break


def view_department_performance():
    """
    View average performance of all batches in a department.
    """
    print_header("Department Performance")
    
    dept_id = safe_input("Enter Department ID: ", validate_id, {"id_type": "Department ID"})
    
    dept_rows = read_csv('Department.csv')
    dept_found = False
    batch_ids = []
    
    for row in dept_rows[1:]:
        if row[0] == dept_id:
            dept_found = True
            batch_ids = row[2].split(':') if row[2] else []
            break
    
    if not dept_found:
        print(f"{ERROR_PREFIX}Department ID not found")
        return
    
    print(f"\n{INFO_PREFIX}Performance Analysis for Department {dept_id}\n")
    print_separator()
    
    from student import read_csv as rc
    from utils import extract_marks_from_string as ems
    
    batch_rows = read_csv(BATCH_FILE)
    student_rows = read_csv('Student.csv')
    course_rows = read_csv('Course.csv')
    
    for batch_id in batch_ids:
        if not batch_id.strip():
            continue
        
        batch_name = ""
        course_ids = []
        
        for batch_row in batch_rows[1:]:
            if batch_row[0] == batch_id:
                batch_name = batch_row[1]
                course_ids = batch_row[3].split('-') if batch_row[3] else []
                break
        
        batch_percentages = []
        
        for student_row in student_rows[1:]:
            if student_row[3] == batch_id:
                student_id = student_row[0]
                
                marks_list = []
                for course_id in course_ids:
                    if not course_id.strip():
                        continue
                    for course_row in course_rows[1:]:
                        if course_row[0] == course_id:
                            marks = ems(course_row[2], student_id)
                            if marks != -1:
                                marks_list.append(marks)
                            break
                
                if marks_list:
                    percentage = calculate_average_marks(marks_list)
                    batch_percentages.append(percentage)
        
        if batch_percentages:
            avg_percentage = calculate_average_marks(batch_percentages)
            print(f"Batch ID:      {batch_id}")
            print(f"Batch Name:    {batch_name}")
            print(f"Avg Percentage: {avg_percentage:.2f}%")
            print(f"Students:      {len(batch_percentages)}")
            print_separator()


def department_statistics():
    """
    Show department statistics.
    """
    print_header("Department Statistics")
    
    dept_rows = read_csv('Department.csv')
    
    print(f"\n{INFO_PREFIX}Total Departments: {len(dept_rows) - 1}\n")
    print_separator()
    
    batch_rows = read_csv(BATCH_FILE)
    
    for row in dept_rows[1:]:
        dept_id = row[0]
        dept_name = row[1]
        batch_ids = row[2].split(':') if row[2] else []
        batch_count = len([b for b in batch_ids if b.strip()])
        
        # Count total students
        student_count = 0
        for batch_id in batch_ids:
            if not batch_id.strip():
                continue
            for batch_row in batch_rows[1:]:
                if batch_row[0] == batch_id:
                    students = batch_row[4].split(':') if batch_row[4] else []
                    student_count += len([s for s in students if s.strip()])
                    break
        
        print(f"Department ID: {dept_id}")
        print(f"Department Name: {dept_name}")
        print(f"Batches:       {batch_count}")
        print(f"Students:      {student_count}")
        print_separator()


def search_department():
    """
    Search for departments by ID or name.
    """
    print_header("Search Department")
    
    search_term = input("Enter Department ID or Name to search: ")
    
    results = search_records('Department.csv', search_term, [0, 1])
    
    if not results:
        print(f"{ERROR_PREFIX}No departments found matching '{search_term}'")
        return
    
    print(f"\n{INFO_PREFIX}Found {len(results)} result(s):\n")
    print_separator()
    
    for idx, row in results:
        print(f"Department ID: {row[0]}")
        print(f"Department Name: {row[1]}")
        print_separator()


def department_menu():
    """
    Display department management menu.
    """
    while True:
        print_header("Department Management")
        print("1. Create a new department")
        print("2. View all batches in a department")
        print("3. View average performance by batch")
        print("4. Show department statistics")
        print("5. Search for a department")
        print("6. Back to main menu")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            create_department()
        elif choice == '2':
            view_department_batches()
        elif choice == '3':
            view_department_performance()
        elif choice == '4':
            department_statistics()
        elif choice == '5':
            search_department()
        elif choice == '6':
            break
        else:
            print(f"{ERROR_PREFIX}Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
