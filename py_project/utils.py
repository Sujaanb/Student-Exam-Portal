"""
Utility functions for the Student Examination Portal
"""

import os
import csv
import pandas as pd
from constants import (
    STUDENT_FILE, COURSE_FILE, BATCH_FILE, DEPARTMENT_FILE,
    STUDENT_HEADERS, COURSE_HEADERS, BATCH_HEADERS, DEPARTMENT_HEADERS,
    SUCCESS_PREFIX, ERROR_PREFIX, INFO_PREFIX
)


def initialize_csv_files():
    """
    Initialize all required CSV files if they don't exist.
    """
    files = [
        (STUDENT_FILE, STUDENT_HEADERS),
        (COURSE_FILE, COURSE_HEADERS),
        (BATCH_FILE, BATCH_HEADERS),
        (DEPARTMENT_FILE, DEPARTMENT_HEADERS),
    ]
    
    for filepath, headers in files:
        if not os.path.isfile(filepath):
            try:
                with open(filepath, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                print(f"{SUCCESS_PREFIX}Created {filepath}")
            except Exception as e:
                print(f"{ERROR_PREFIX}Failed to create {filepath}: {str(e)}")


def read_csv(filename):
    """
    Read CSV file and return list of rows.
    
    Args:
        filename (str): Path to CSV file
        
    Returns:
        list: List of rows (each row is a list)
    """
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        return rows
    except FileNotFoundError:
        print(f"{ERROR_PREFIX}File {filename} not found")
        return []
    except Exception as e:
        print(f"{ERROR_PREFIX}Error reading {filename}: {str(e)}")
        return []


def write_csv(filename, rows):
    """
    Write list of rows to CSV file.
    
    Args:
        filename (str): Path to CSV file
        rows (list): List of rows to write
    """
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    except Exception as e:
        print(f"{ERROR_PREFIX}Error writing to {filename}: {str(e)}")


def append_to_csv(filename, row):
    """
    Append a single row to CSV file.
    
    Args:
        filename (str): Path to CSV file
        row (list): Row to append
    """
    try:
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    except Exception as e:
        print(f"{ERROR_PREFIX}Error appending to {filename}: {str(e)}")


def update_csv_cell(filename, row_index, col_index, value):
    """
    Update a specific cell in CSV file.
    
    Args:
        filename (str): Path to CSV file
        row_index (int): Row index (0-based)
        col_index (int): Column index (0-based)
        value: New value
    """
    try:
        df = pd.read_csv(filename)
        df.iloc[row_index, col_index] = value
        df.to_csv(filename, index=False)
    except Exception as e:
        print(f"{ERROR_PREFIX}Error updating {filename}: {str(e)}")


def find_row_index(filename, column_index, value):
    """
    Find row index by column value.
    
    Args:
        filename (str): Path to CSV file
        column_index (int): Column index to search
        value: Value to find
        
    Returns:
        int: Row index if found, -1 otherwise
    """
    try:
        rows = read_csv(filename)
        for i, row in enumerate(rows):
            if i > 0 and len(row) > column_index and row[column_index] == value:
                return i
        return -1
    except Exception as e:
        print(f"{ERROR_PREFIX}Error searching {filename}: {str(e)}")
        return -1


def remove_row(filename, row_index):
    """
    Remove a row from CSV file.
    
    Args:
        filename (str): Path to CSV file
        row_index (int): Row index to remove
    """
    try:
        rows = read_csv(filename)
        if 0 < row_index < len(rows):
            del rows[row_index]
            write_csv(filename, rows)
            return True
        return False
    except Exception as e:
        print(f"{ERROR_PREFIX}Error removing row from {filename}: {str(e)}")
        return False


def search_records(filename, search_term, column_indices):
    """
    Search for records in CSV file across multiple columns.
    
    Args:
        filename (str): Path to CSV file
        search_term (str): Term to search for
        column_indices (list): List of column indices to search
        
    Returns:
        list: List of matching rows with their indices
    """
    results = []
    try:
        rows = read_csv(filename)
        search_term_lower = search_term.lower()
        
        for i, row in enumerate(rows):
            if i == 0:  # Skip header
                continue
            for col_idx in column_indices:
                if col_idx < len(row) and search_term_lower in row[col_idx].lower():
                    results.append((i, row))
                    break
        return results
    except Exception as e:
        print(f"{ERROR_PREFIX}Error searching {filename}: {str(e)}")
        return []


def extract_marks_from_string(marks_string, student_id):
    """
    Extract marks for a specific student from delimited string.
    
    Args:
        marks_string (str): Delimited marks string (e.g., "S1:85-S2:90")
        student_id (str): Student ID to extract marks for
        
    Returns:
        int: Marks if found, -1 otherwise
    """
    try:
        parts = marks_string.split('-')
        for part in parts:
            if ':' in part:
                sid, marks = part.split(':')
                if sid == student_id:
                    return int(marks)
        return -1
    except Exception as e:
        print(f"{ERROR_PREFIX}Error extracting marks: {str(e)}")
        return -1


def calculate_average_marks(marks_list):
    """
    Calculate average from list of marks.
    
    Args:
        marks_list (list): List of marks
        
    Returns:
        float: Average marks, 0 if list is empty
    """
    if not marks_list or len(marks_list) == 0:
        return 0
    return sum(marks_list) / len(marks_list)


def get_grade(percentage):
    """
    Get grade letter based on percentage.
    
    Args:
        percentage (float): Percentage score
        
    Returns:
        str: Grade letter (A-F)
    """
    if percentage >= 90:
        return 'A'
    elif percentage >= 80:
        return 'B'
    elif percentage >= 70:
        return 'C'
    elif percentage >= 60:
        return 'D'
    elif percentage >= 40:
        return 'E'
    else:
        return 'F'


def get_pass_status(percentage, pass_threshold=40):
    """
    Determine if student passed.
    
    Args:
        percentage (float): Percentage score
        pass_threshold (int): Passing threshold
        
    Returns:
        str: "PASS" or "FAIL"
    """
    return "PASS" if percentage >= pass_threshold else "FAIL"


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """
    Print a formatted header.
    
    Args:
        title (str): Title to display
    """
    print("\n" + "=" * 60)
    print(f"  {title.center(56)}")
    print("=" * 60 + "\n")


def print_separator():
    """Print a separator line."""
    print("-" * 60)


def confirm_action(action_description):
    """
    Ask user to confirm an action.
    
    Args:
        action_description (str): Description of action
        
    Returns:
        bool: True if confirmed, False otherwise
    """
    response = input(f"\n⚠️  {action_description}? (y/n): ").strip().lower()
    return response in ('y', 'yes')
