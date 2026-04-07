"""
Examination Management Module for the Student Examination Portal
"""

from constants import (
    STUDENT_FILE, COURSE_FILE, ERROR_PREFIX, SUCCESS_PREFIX, INFO_PREFIX,
    SCATTER_PLOT_COLORS
)
from utils import (
    read_csv, extract_marks_from_string, calculate_average_marks,
    print_header, print_separator
)
from validators import safe_input, validate_id
import matplotlib.pyplot as plt


def view_overall_performance():
    """
    View overall performance of all students in the examination.
    """
    print_header("Overall Examination Performance")
    
    student_rows = read_csv(STUDENT_FILE)
    course_rows = read_csv(COURSE_FILE)
    
    print(f"\n{INFO_PREFIX}Overall Performance Analysis\n")
    print_separator()
    
    for student_row in student_rows[1:]:
        student_id = student_row[0]
        name = student_row[1]
        
        marks_list = []
        for course_row in course_rows[1:]:
            marks = extract_marks_from_string(course_row[2], student_id)
            if marks != -1:
                marks_list.append(marks)
        
        if marks_list:
            overall_percentage = calculate_average_marks(marks_list)
            print(f"Student ID:    {student_id}")
            print(f"Name:          {name}")
            print(f"Overall %:     {overall_percentage:.2f}%")
            print_separator()


def examination_statistics():
    """
    Show examination statistics with scatter plot.
    """
    print_header("Examination Statistics")
    
    course_rows = read_csv(COURSE_FILE)
    student_rows = read_csv(STUDENT_FILE)
    
    student_dict = {row[0]: row[1] for row in student_rows[1:]}
    
    course_marks = {}
    
    for course_row in course_rows[1:]:
        if course_row[2]:
            course_id = course_row[0]
            marks_data = []
            
            mark_parts = course_row[2].split('-')
            for part in mark_parts:
                if ':' in part:
                    sid, marks = part.split(':')
                    try:
                        marks_data.append(int(marks))
                    except ValueError:
                        pass
            
            if marks_data:
                course_marks[course_id] = marks_data
    
    if not course_marks:
        print(f"{ERROR_PREFIX}No marks data available")
        return
    
    # Create scatter plot
    plt.figure(figsize=(12, 8))
    
    colors = SCATTER_PLOT_COLORS[:len(course_marks)]
    x_pos = 1
    
    for idx, (course_id, marks) in enumerate(course_marks.items()):
        y_values = marks
        x_values = [x_pos] * len(y_values)
        plt.scatter(x_values, y_values, c=colors[idx], label=f"Course {course_id}", s=100, alpha=0.6)
        x_pos += 1
    
    plt.xlabel('Courses')
    plt.ylabel('Marks Obtained')
    plt.title('Examination Statistics - Marks Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Print statistics
    print(f"\n{INFO_PREFIX}Course-wise Statistics:\n")
    print_separator()
    
    for course_id, marks in course_marks.items():
        avg_marks = calculate_average_marks(marks)
        max_marks = max(marks)
        min_marks = min(marks)
        
        print(f"Course ID:     {course_id}")
        print(f"Students:      {len(marks)}")
        print(f"Avg Marks:     {avg_marks:.2f}")
        print(f"Max Marks:     {max_marks}")
        print(f"Min Marks:     {min_marks}")
        print_separator()


def examination_menu():
    """
    Display examination management menu.
    """
    while True:
        print_header("Examination Management")
        print("1. View overall student performance")
        print("2. Show examination statistics (scatter plot)")
        print("3. Back to main menu")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            view_overall_performance()
        elif choice == '2':
            examination_statistics()
        elif choice == '3':
            break
        else:
            print(f"{ERROR_PREFIX}Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
