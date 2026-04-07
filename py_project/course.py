"""
Course Management Module for the Student Examination Portal
"""

from constants import (
    COURSE_FILE, BATCH_FILE, STUDENT_FILE, ERROR_PREFIX, SUCCESS_PREFIX, INFO_PREFIX
)
from utils import (
    read_csv, write_csv, append_to_csv, find_row_index, search_records,
    extract_marks_from_string, print_header, print_separator,
    confirm_action, calculate_average_marks
)
from validators import validate_id, validate_name, validate_marks, safe_input
import pandas as pd


def create_course():
    """
    Create a new course.
    """
    print_header("Create New Course")
    
    while True:
        # Get Course ID
        course_id = safe_input("Enter Course ID: ", validate_id, {"id_type": "Course ID"})
        
        # Check if course already exists
        rows = read_csv(COURSE_FILE)
        existing_ids = [row[0] for row in rows[1:]]
        
        if course_id in existing_ids:
            print(f"{ERROR_PREFIX}Course ID already exists")
            continue
        
        # Get Course Name
        course_name = safe_input("Enter Course Name: ", validate_name)
        
        # Get Batch ID
        batch_rows = read_csv(BATCH_FILE)
        batch_ids = [row[0] for row in batch_rows[1:]]
        
        while True:
            batch_id = safe_input("Enter Batch ID: ", validate_id, {"id_type": "Batch ID"})
            if batch_id not in batch_ids:
                print(f"{ERROR_PREFIX}Batch ID does not exist")
                continue
            break
        
        # Get students in this batch
        student_ids = []
        for batch_row in batch_rows:
            if batch_row[0] == batch_id:
                student_ids = batch_row[4].split(':') if batch_row[4] else []
                break
        
        # Enter marks for each student
        marks_string = ""
        for student_id in student_ids:
            if not student_id.strip():
                continue
            
            while True:
                marks_input = safe_input(f"Enter marks for Student ID {student_id}: ")
                is_valid, error_msg, marks = validate_marks(marks_input)
                if is_valid:
                    break
                if error_msg:
                    print(error_msg)
            
            if marks_string:
                marks_string += f"-{student_id}:{marks}"
            else:
                marks_string = f"{student_id}:{marks}"
        
        # Add course to Course.csv
        append_to_csv(COURSE_FILE, [course_id, course_name, marks_string])
        
        # Update Batch.csv
        batch_rows = read_csv(BATCH_FILE)
        for i, row in enumerate(batch_rows):
            if row[0] == batch_id:
                if row[3]:  # Existing courses
                    row[3] = f"{row[3]}-{course_id}"
                else:
                    row[3] = course_id
                batch_rows[i] = row
                break
        write_csv(BATCH_FILE, batch_rows)
        
        print(f"\n{SUCCESS_PREFIX}Course created successfully!")
        
        if not confirm_action("Create another course"):
            break


def view_course_performance():
    """
    View student performance in a course.
    """
    print_header("Course Performance")
    
    course_id = safe_input("Enter Course ID: ", validate_id, {"id_type": "Course ID"})
    
    course_rows = read_csv(COURSE_FILE)
    course_found = False
    
    for row in course_rows[1:]:
        if row[0] == course_id:
            course_found = True
            course_name = row[1]
            marks_string = row[2]
            break
    
    if not course_found:
        print(f"{ERROR_PREFIX}Course ID not found")
        return
    
    print(f"\n{INFO_PREFIX}Course: {course_name} ({course_id})\n")
    print_separator()
    
    student_rows = read_csv(STUDENT_FILE)
    student_dict = {row[0]: row[1] for row in student_rows[1:]}
    
    mark_parts = marks_string.split('-')
    total_marks = 0
    student_count = 0
    
    for part in mark_parts:
        if ':' in part:
            student_id, marks = part.split(':')
            marks = int(marks)
            student_name = student_dict.get(student_id, "Unknown")
            
            print(f"Student ID:    {student_id}")
            print(f"Student Name:  {student_name}")
            print(f"Marks:         {marks}")
            print_separator()
            
            total_marks += marks
            student_count += 1
    
    if student_count > 0:
        avg_marks = total_marks / student_count
        print(f"\nAverage Marks: {avg_marks:.2f}")
        print(f"Total Students: {student_count}")


def course_statistics():
    """
    Show course statistics.
    """
    print_header("Course Statistics")
    
    course_rows = read_csv(COURSE_FILE)
    
    print(f"\n{INFO_PREFIX}Total Courses: {len(course_rows) - 1}\n")
    print_separator()
    
    for row in course_rows[1:]:
        course_id = row[0]
        course_name = row[1]
        marks_string = row[2]
        
        mark_parts = marks_string.split('-') if marks_string else []
        student_count = len([p for p in mark_parts if p])
        
        if student_count > 0:
            total_marks = sum([int(p.split(':')[1]) for p in mark_parts if ':' in p])
            avg_marks = total_marks / student_count
        else:
            avg_marks = 0
        
        print(f"Course ID:     {course_id}")
        print(f"Course Name:   {course_name}")
        print(f"Students:      {student_count}")
        print(f"Avg Marks:     {avg_marks:.2f}")
        print_separator()


def search_course():
    """
    Search for courses by ID or name.
    """
    print_header("Search Course")
    
    search_term = input("Enter Course ID or Name to search: ")
    
    results = search_records(COURSE_FILE, search_term, [0, 1])
    
    if not results:
        print(f"{ERROR_PREFIX}No courses found matching '{search_term}'")
        return
    
    print(f"\n{INFO_PREFIX}Found {len(results)} result(s):\n")
    print_separator()
    
    for idx, row in results:
        print(f"Course ID:     {row[0]}")
        print(f"Course Name:   {row[1]}")
        print(f"Marks Data:    {row[2][:50]}..." if len(row[2]) > 50 else f"Marks Data:    {row[2]}")
        print_separator()


def course_menu():
    """
    Display course management menu.
    """
    while True:
        print_header("Course Management")
        print("1. Create a new course")
        print("2. View student performance in course")
        print("3. Show course statistics")
        print("4. Search for a course")
        print("5. Back to main menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            create_course()
        elif choice == '2':
            view_course_performance()
        elif choice == '3':
            course_statistics()
        elif choice == '4':
            search_course()
        elif choice == '5':
            break
        else:
            print(f"{ERROR_PREFIX}Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
