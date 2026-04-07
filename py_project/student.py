"""
Student Management Module for the Student Examination Portal
"""

from constants import (
    STUDENT_FILE, COURSE_FILE, BATCH_FILE, ERROR_PREFIX, SUCCESS_PREFIX, INFO_PREFIX
)
from utils import (
    read_csv, write_csv, append_to_csv, find_row_index, remove_row,
    search_records, extract_marks_from_string, calculate_average_marks,
    get_grade, get_pass_status, print_header, print_separator,
    confirm_action, update_csv_cell
)
from validators import validate_id, validate_name, validate_marks, validate_roll_number, safe_input
import pandas as pd


def create_student():
    """
    Create a new student record.
    """
    print_header("Create New Student")
    
    while True:
        # Get Student ID
        student_id = safe_input("Enter Student ID: ", validate_id, {"id_type": "Student ID"})
        
        # Check if student already exists
        rows = read_csv(STUDENT_FILE)
        existing_ids = [row[0] for row in rows[1:]]
        
        if student_id in existing_ids:
            print(f"{ERROR_PREFIX}Student ID already exists")
            continue
        
        # Get Student Name
        name = safe_input("Enter Student Name: ", validate_name)
        
        # Get Roll Number
        roll_no = safe_input("Enter Class Roll Number: ", validate_roll_number)
        
        # Get Batch ID
        batch_rows = read_csv(BATCH_FILE)
        batch_ids = [row[0] for row in batch_rows[1:]]
        
        while True:
            batch_id = safe_input("Enter Batch ID: ", validate_id, {"id_type": "Batch ID"})
            if batch_id not in batch_ids:
                print(f"{ERROR_PREFIX}Batch ID does not exist. Please create the batch first.")
                continue
            break
        
        # Get course IDs for this batch
        course_ids = []
        for batch_row in batch_rows:
            if batch_row[0] == batch_id:
                course_ids = batch_row[3].split('-') if batch_row[3] else []
                break
        
        # Enter marks for each course
        marks_string = ""
        course_rows = read_csv(COURSE_FILE)
        
        for course_id in course_ids:
            if not course_id.strip():
                continue
            
            # Find course name
            course_name = course_id
            for row in course_rows[1:]:
                if row[0] == course_id:
                    course_name = row[1]
                    break
            
            while True:
                marks_input = safe_input(f"Enter marks for {course_name} ({course_id}): ")
                is_valid, error_msg, marks_int = validate_marks(marks_input)
                if is_valid:
                    marks = marks_int
                    break
                if error_msg:
                    print(error_msg)
            
            if marks_string:
                marks_string += f"-{student_id}:{marks}"
            else:
                marks_string = f"{student_id}:{marks}"
            
            # Update course file with student marks
            for i, row in enumerate(course_rows):
                if row[0] == course_id:
                    existing_marks = row[2]
                    if existing_marks:
                        row[2] = f"{existing_marks}-{student_id}:{marks}"
                    else:
                        row[2] = f"{student_id}:{marks}"
                    course_rows[i] = row
                    break
        
        write_csv(COURSE_FILE, course_rows)
        
        # Add student to Student.csv
        append_to_csv(STUDENT_FILE, [student_id, name, roll_no, batch_id])
        
        # Update Batch.csv with student list
        batch_rows = read_csv(BATCH_FILE)
        for i, row in enumerate(batch_rows):
            if row[0] == batch_id:
                if row[4]:  # Existing students
                    row[4] = f"{row[4]}:{student_id}"
                else:
                    row[4] = student_id
                batch_rows[i] = row
                break
        write_csv(BATCH_FILE, batch_rows)
        
        print(f"\n{SUCCESS_PREFIX}Student created successfully!")
        
        if not confirm_action("Add another student"):
            break


def update_student():
    """
    Update existing student details.
    """
    print_header("Update Student Details")
    
    while True:
        student_id = safe_input("Enter Student ID to update: ", validate_id, {"id_type": "Student ID"})
        
        rows = read_csv(STUDENT_FILE)
        row_idx = find_row_index(STUDENT_FILE, 0, student_id)
        
        if row_idx == -1:
            print(f"{ERROR_PREFIX}Student ID not found")
            continue
        
        print(f"\n{INFO_PREFIX}Current Details:")
        print(f"  Name: {rows[row_idx][1]}")
        print(f"  Roll No: {rows[row_idx][2]}")
        print(f"  Batch ID: {rows[row_idx][3]}")
        
        name = safe_input("Enter new Student Name: ", validate_name)
        roll_no = safe_input("Enter new Class Roll Number: ", validate_roll_number)
        
        rows[row_idx][1] = name
        rows[row_idx][2] = roll_no
        write_csv(STUDENT_FILE, rows)
        
        print(f"\n{SUCCESS_PREFIX}Student updated successfully!")
        
        if not confirm_action("Update another student"):
            break


def delete_student():
    """
    Remove a student from the database.
    """
    print_header("Delete Student")
    
    while True:
        student_id = safe_input("Enter Student ID to delete: ", validate_id, {"id_type": "Student ID"})
        
        row_idx = find_row_index(STUDENT_FILE, 0, student_id)
        if row_idx == -1:
            print(f"{ERROR_PREFIX}Student ID not found")
            continue
        
        if not confirm_action(f"Delete student {student_id}"):
            continue
        
        # Remove from Student.csv
        remove_row(STUDENT_FILE, row_idx)
        
        # Remove from Course.csv marks
        course_rows = read_csv(COURSE_FILE)
        for i, row in enumerate(course_rows[1:], 1):
            marks = row[2]
            if student_id in marks:
                # Parse and remove student marks
                mark_parts = marks.split('-')
                filtered_marks = [m for m in mark_parts if not m.startswith(f"{student_id}:")]
                course_rows[i][2] = '-'.join(filtered_marks)
        write_csv(COURSE_FILE, course_rows)
        
        # Remove from Batch.csv students list
        batch_rows = read_csv(BATCH_FILE)
        for i, row in enumerate(batch_rows[1:], 1):
            students = row[4]
            if student_id in students:
                student_list = students.split(':')
                filtered_students = [s for s in student_list if s != student_id]
                batch_rows[i][4] = ':'.join(filtered_students)
        write_csv(BATCH_FILE, batch_rows)
        
        print(f"\n{SUCCESS_PREFIX}Student deleted successfully!")
        
        if not confirm_action("Delete another student"):
            break


def generate_report_card():
    """
    Generate a report card for a student.
    """
    print_header("Generate Report Card")
    
    student_id = safe_input("Enter Student ID: ", validate_id, {"id_type": "Student ID"})
    
    row_idx = find_row_index(STUDENT_FILE, 0, student_id)
    if row_idx == -1:
        print(f"{ERROR_PREFIX}Student ID not found")
        return
    
    student_rows = read_csv(STUDENT_FILE)
    student_data = student_rows[row_idx]
    name = student_data[1]
    roll_no = student_data[2]
    batch_id = student_data[3]
    
    # Get batch details
    batch_rows = read_csv(BATCH_FILE)
    course_ids = []
    for row in batch_rows:
        if row[0] == batch_id:
            course_ids = row[3].split('-') if row[3] else []
            break
    
    # Calculate marks
    course_rows = read_csv(COURSE_FILE)
    marks_list = []
    
    for course_id in course_ids:
        if not course_id.strip():
            continue
        for row in course_rows:
            if row[0] == course_id:
                marks = extract_marks_from_string(row[2], student_id)
                if marks != -1:
                    marks_list.append(marks)
                break
    
    if not marks_list:
        print(f"{ERROR_PREFIX}No marks found for this student")
        return
    
    percentage = calculate_average_marks(marks_list)
    grade = get_grade(percentage)
    status = get_pass_status(percentage)
    
    # Generate report
    report = f"""
{'='*60}
{'REPORT CARD'.center(60)}
{'='*60}

Student ID:        {student_id}
Student Name:      {name}
Class Roll No.:    {roll_no}
Batch ID:          {batch_id}
Percentage:        {percentage:.2f}%
Overall Grade:     {grade}
Passing Status:    {status}

{'='*60}
"""
    
    print(report)
    
    # Save to file
    with open('result.txt', 'w') as f:
        f.write(report)
    print(f"{SUCCESS_PREFIX}Report card saved to result.txt")


def search_student():
    """
    Search for students by ID or name.
    """
    print_header("Search Student")
    
    search_term = input("Enter Student ID or Name to search: ")
    
    results = search_records(STUDENT_FILE, search_term, [0, 1])
    
    if not results:
        print(f"{ERROR_PREFIX}No students found matching '{search_term}'")
        return
    
    print(f"\n{INFO_PREFIX}Found {len(results)} result(s):\n")
    print_separator()
    
    for idx, row in results:
        print(f"Student ID:    {row[0]}")
        print(f"Name:          {row[1]}")
        print(f"Roll No:       {row[2]}")
        print(f"Batch ID:      {row[3]}")
        print_separator()


def student_menu():
    """
    Display student management menu.
    """
    while True:
        print_header("Student Management")
        print("1. Create a new student")
        print("2. Update student details")
        print("3. Delete a student")
        print("4. Generate report card")
        print("5. Search for a student")
        print("6. Back to main menu")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            create_student()
        elif choice == '2':
            update_student()
        elif choice == '3':
            delete_student()
        elif choice == '4':
            generate_report_card()
        elif choice == '5':
            search_student()
        elif choice == '6':
            break
        else:
            print(f"{ERROR_PREFIX}Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
