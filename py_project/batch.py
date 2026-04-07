"""
Batch Management Module for the Student Examination Portal
"""

from constants import (
    BATCH_FILE, STUDENT_FILE, COURSE_FILE, ERROR_PREFIX, SUCCESS_PREFIX, INFO_PREFIX,
    PIE_CHART_COLORS
)
from utils import (
    read_csv, write_csv, append_to_csv, find_row_index, search_records,
    extract_marks_from_string, calculate_average_marks, get_grade,
    print_header, print_separator, confirm_action
)
from validators import validate_id, validate_name, safe_input
import matplotlib.pyplot as plt


def create_batch():
    """
    Create a new batch.
    """
    print_header("Create New Batch")
    
    while True:
        # Get Batch ID
        batch_id = safe_input("Enter Batch ID: ", validate_id, {"id_type": "Batch ID"})
        
        # Check if batch already exists
        rows = read_csv(BATCH_FILE)
        existing_ids = [row[0] for row in rows[1:]]
        
        if batch_id in existing_ids:
            print(f"{ERROR_PREFIX}Batch ID already exists")
            continue
        
        # Get Batch Name
        batch_name = safe_input("Enter Batch Name: ", validate_name)
        
        # Get Department
        dept_rows = read_csv('Department.csv')
        dept_names = [row[1] for row in dept_rows[1:]]
        
        while True:
            dept_name = safe_input("Enter Department Name: ", validate_name)
            if dept_name not in dept_names:
                print(f"{ERROR_PREFIX}Department does not exist. Please create it first.")
                continue
            break
        
        # Add batch
        append_to_csv(BATCH_FILE, [batch_id, batch_name, dept_name, '', ''])
        
        # Update Department.csv
        dept_rows = read_csv('Department.csv')
        for i, row in enumerate(dept_rows):
            if row[1] == dept_name:
                if row[2]:
                    row[2] = f"{row[2]}:{batch_id}"
                else:
                    row[2] = batch_id
                dept_rows[i] = row
                break
        write_csv('Department.csv', dept_rows)
        
        print(f"\n{SUCCESS_PREFIX}Batch created successfully!")
        
        if not confirm_action("Create another batch"):
            break


def view_batch_students():
    """
    View all students in a batch.
    """
    print_header("Batch Students")
    
    batch_id = safe_input("Enter Batch ID: ", validate_id, {"id_type": "Batch ID"})
    
    batch_rows = read_csv(BATCH_FILE)
    batch_found = False
    
    for row in batch_rows[1:]:
        if row[0] == batch_id:
            batch_found = True
            batch_name = row[1]
            break
    
    if not batch_found:
        print(f"{ERROR_PREFIX}Batch ID not found")
        return
    
    print(f"\n{INFO_PREFIX}Batch: {batch_name}\n")
    print_separator()
    
    student_rows = read_csv(STUDENT_FILE)
    student_count = 0
    
    for row in student_rows[1:]:
        if row[3] == batch_id:
            print(f"Student ID:    {row[0]}")
            print(f"Name:          {row[1]}")
            print(f"Roll No:       {row[2]}")
            print_separator()
            student_count += 1
    
    if student_count == 0:
        print(f"{INFO_PREFIX}No students in this batch")


def view_batch_courses():
    """
    View all courses taught in a batch.
    """
    print_header("Batch Courses")
    
    batch_id = safe_input("Enter Batch ID: ", validate_id, {"id_type": "Batch ID"})
    
    batch_rows = read_csv(BATCH_FILE)
    batch_found = False
    course_ids = []
    
    for row in batch_rows[1:]:
        if row[0] == batch_id:
            batch_found = True
            course_ids = row[3].split('-') if row[3] else []
            break
    
    if not batch_found:
        print(f"{ERROR_PREFIX}Batch ID not found")
        return
    
    print(f"\n{INFO_PREFIX}Courses in Batch {batch_id}:\n")
    print_separator()
    
    course_rows = read_csv(COURSE_FILE)
    
    for course_id in course_ids:
        if not course_id.strip():
            continue
        
        for row in course_rows[1:]:
            if row[0] == course_id:
                print(f"Course ID:     {row[0]}")
                print(f"Course Name:   {row[1]}")
                print_separator()
                break


def view_batch_performance():
    """
    View complete performance of all students in a batch.
    """
    print_header("Batch Performance")
    
    batch_id = safe_input("Enter Batch ID: ", validate_id, {"id_type": "Batch ID"})
    
    batch_rows = read_csv(BATCH_FILE)
    batch_found = False
    course_ids = []
    
    for row in batch_rows[1:]:
        if row[0] == batch_id:
            batch_found = True
            course_ids = row[3].split('-') if row[3] else []
            break
    
    if not batch_found:
        print(f"{ERROR_PREFIX}Batch ID not found")
        return
    
    print(f"\n{INFO_PREFIX}Performance Analysis for Batch {batch_id}\n")
    print_separator()
    
    student_rows = read_csv(STUDENT_FILE)
    course_rows = read_csv(COURSE_FILE)
    
    for student_row in student_rows[1:]:
        if student_row[3] == batch_id:
            student_id = student_row[0]
            name = student_row[1]
            
            marks_list = []
            for course_id in course_ids:
                if not course_id.strip():
                    continue
                for course_row in course_rows[1:]:
                    if course_row[0] == course_id:
                        marks = extract_marks_from_string(course_row[2], student_id)
                        if marks != -1:
                            marks_list.append(marks)
                        break
            
            if marks_list:
                percentage = calculate_average_marks(marks_list)
                print(f"Student ID:    {student_id}")
                print(f"Name:          {name}")
                print(f"Percentage:    {percentage:.2f}%")
                print_separator()


def view_grade_distribution():
    """
    Display pie chart of grade distribution for batch.
    """
    print_header("Batch Grade Distribution")
    
    batch_id = safe_input("Enter Batch ID: ", validate_id, {"id_type": "Batch ID"})
    
    batch_rows = read_csv(BATCH_FILE)
    batch_found = False
    course_ids = []
    
    for row in batch_rows[1:]:
        if row[0] == batch_id:
            batch_found = True
            course_ids = row[3].split('-') if row[3] else []
            break
    
    if not batch_found:
        print(f"{ERROR_PREFIX}Batch ID not found")
        return
    
    student_rows = read_csv(STUDENT_FILE)
    course_rows = read_csv(COURSE_FILE)
    
    grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}
    
    for student_row in student_rows[1:]:
        if student_row[3] == batch_id:
            student_id = student_row[0]
            
            marks_list = []
            for course_id in course_ids:
                if not course_id.strip():
                    continue
                for course_row in course_rows[1:]:
                    if course_row[0] == course_id:
                        marks = extract_marks_from_string(course_row[2], student_id)
                        if marks != -1:
                            marks_list.append(marks)
                        break
            
            if marks_list:
                percentage = calculate_average_marks(marks_list)
                grade = get_grade(percentage)
                grade_distribution[grade] += 1
    
    # Create pie chart
    grades = [g for g in grade_distribution.keys() if grade_distribution[g] > 0]
    counts = [grade_distribution[g] for g in grades]
    
    if not grades:
        print(f"{ERROR_PREFIX}No grade data available for this batch")
        return
    
    colors = PIE_CHART_COLORS[:len(grades)]
    plt.figure(figsize=(10, 6))
    plt.pie(counts, labels=grades, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title(f'Grade Distribution - Batch {batch_id}')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def search_batch():
    """
    Search for batches by ID or name.
    """
    print_header("Search Batch")
    
    search_term = input("Enter Batch ID or Name to search: ")
    
    results = search_records(BATCH_FILE, search_term, [0, 1])
    
    if not results:
        print(f"{ERROR_PREFIX}No batches found matching '{search_term}'")
        return
    
    print(f"\n{INFO_PREFIX}Found {len(results)} result(s):\n")
    print_separator()
    
    for idx, row in results:
        print(f"Batch ID:      {row[0]}")
        print(f"Batch Name:    {row[1]}")
        print(f"Department:    {row[2]}")
        print_separator()


def batch_menu():
    """
    Display batch management menu.
    """
    while True:
        print_header("Batch Management")
        print("1. Create a new batch")
        print("2. View all students in a batch")
        print("3. View all courses in a batch")
        print("4. View complete performance of all students")
        print("5. View grade distribution pie chart")
        print("6. Search for a batch")
        print("7. Back to main menu")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            create_batch()
        elif choice == '2':
            view_batch_students()
        elif choice == '3':
            view_batch_courses()
        elif choice == '4':
            view_batch_performance()
        elif choice == '5':
            view_grade_distribution()
        elif choice == '6':
            search_batch()
        elif choice == '7':
            break
        else:
            print(f"{ERROR_PREFIX}Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
