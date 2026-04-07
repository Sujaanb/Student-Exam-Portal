# Utility functions for Student Exam Portal
# Centralizes common operations and reduces code duplication

import csv
import pandas as pd
from config import FILES, PASS_THRESHOLD, get_grade

def read_csv(filename):
    """Read a CSV file and return list of rows"""
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        return rows
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return []
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []

def get_column_values(filename, column_index):
    """Extract values from a specific column of a CSV file"""
    rows = read_csv(filename)
    if not rows:
        return []
    return [row[column_index] for row in rows if len(row) > column_index]

def check_id_exists(filename, column_index, id_value):
    """Check if an ID exists in a CSV file"""
    rows = read_csv(filename)
    for row in rows:
        if len(row) > column_index and row[column_index] == id_value:
            return True
    return False

def get_valid_marks(prompt="Enter marks: "):
    """Get validated marks input (0-100 range)"""
    while True:
        try:
            marks = int(input(prompt))
            if 0 <= marks <= 100:
                return marks
            else:
                print("Error: Marks must be between 0 and 100")
        except ValueError:
            print("Error: Please enter a valid number")

def get_valid_input(prompt, valid_options):
    """Get validated input from predefined options"""
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() in [opt.lower() for opt in valid_options]:
            return user_input
        print(f"Invalid input. Please choose from: {', '.join(valid_options)}")

def parse_marks_string(marks_string, student_id):
    """Extract marks for a specific student from marks string"""
    marks_str = ''
    parts = marks_string.split('-')
    for part in parts:
        if student_id in part:
            # Extract marks after the colon
            if ':' in part:
                marks_str = part.split(':')[1]
            break
    return int(marks_str) if marks_str.isdigit() else 0

def calculate_percentage(marks_list):
    """Calculate percentage from a list of marks"""
    if not marks_list:
        return 0
    return (sum(marks_list) / len(marks_list))

def get_passing_status(percentage):
    """Determine if student passes based on percentage"""
    return 'PASS' if percentage >= PASS_THRESHOLD else 'FAIL'

def help1(student_ids, course_ids):
    """
    Calculate average percentage for each student across multiple courses
    (Replaces complex logic from main code)
    """
    try:
        percentages = []
        for student_id in student_ids:
            total_marks = 0
            valid_courses = 0
            
            for course_id in course_ids:
                with open(FILES['COURSE'], 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) > 0 and row[0] == course_id:
                            if len(row) > 2:
                                marks = parse_marks_string(row[2], student_id)
                                if marks > 0:
                                    total_marks += marks
                                    valid_courses += 1
                            break
            
            percentage = (total_marks / valid_courses) if valid_courses > 0 else 0
            percentages.append(percentage)
        
        return percentages
    except Exception as e:
        print(f"Error calculating percentages: {e}")
        return []

def help2(marks_string, student_id):
    """
    Extract marks for a specific student from marks string
    (Replaces complex logic from main code)
    """
    try:
        marks_str = ''
        parts = marks_string.partition(student_id)
        if parts[1]:  # If student_id found
            remaining = parts[2]
            for char in remaining[1:]:  # Skip the first colon
                if char.isdigit():
                    marks_str += char
                else:
                    break
            return int(marks_str) if marks_str else 0
        return 0
    except Exception as e:
        print(f"Error extracting marks: {e}")
        return 0

def generate_report_card(student_id, name, roll_no, batch_id, percentage, grade, status):
    """Generate and display report card"""
    report = [
        "=" * 50,
        "REPORT CARD",
        "=" * 50,
        f"Student ID: {student_id}",
        f"Student Name: {name}",
        f"Student Roll No.: {roll_no}",
        f"Batch ID: {batch_id}",
        f"Percentage: {percentage:.2f}%",
        f"Overall Grade: {grade}",
        f"Passing Status: {status}",
        "=" * 50
    ]
    
    report_text = '\n'.join(report)
    
    # Display to console
    print(report_text)
    
    # Save to file
    try:
        with open('result.txt', 'w+') as res:
            res.write(report_text)
        print("\nReport saved to result.txt")
    except Exception as e:
        print(f"Error saving report: {e}")
    
    return report_text

def initialize_csv_files():
    """Initialize CSV files if they don't exist"""
    # Student CSV
    if not csv_file_exists(FILES['STUDENT']):
        with open(FILES['STUDENT'], 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Student ID', 'Name', 'Class Roll No.', 'Batch ID'])
    
    # Course CSV
    if not csv_file_exists(FILES['COURSE']):
        with open(FILES['COURSE'], 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Course ID', 'Course Name', 'Marks Obtained'])
    
    # Batch CSV
    if not csv_file_exists(FILES['BATCH']):
        with open(FILES['BATCH'], 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Batch ID', 'Batch Name', 'Department Name', 'List of Courses', 'List of Students'])
    
    # Department CSV
    if not csv_file_exists(FILES['DEPARTMENT']):
        with open(FILES['DEPARTMENT'], 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Department ID', 'Department Name', 'List of batches'])

def csv_file_exists(filename):
    """Check if CSV file exists and is not empty"""
    import os
    return os.path.isfile(filename)
