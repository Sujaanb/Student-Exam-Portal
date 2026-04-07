# Configuration file for Student Exam Portal
# Centralized constants and file paths

# CSV File paths
FILES = {
    'STUDENT': 'Student.csv',
    'COURSE': 'Course.csv',
    'BATCH': 'Batch.csv',
    'DEPARTMENT': 'Department.csv'
}

# Column definitions for each CSV file
COLUMNS = {
    'STUDENT': ['Student ID', 'Name', 'Class Roll No.', 'Batch ID'],
    'COURSE': ['Course ID', 'Course Name', 'Marks Obtained'],
    'BATCH': ['Batch ID', 'Batch Name', 'Department Name', 'List of Courses', 'List of Students'],
    'DEPARTMENT': ['Department ID', 'Department Name', 'List of batches']
}

# Grade mapping for report cards
GRADES = {
    'A': (90, 100),
    'B': (80, 89),
    'C': (70, 79),
    'D': (60, 69),
    'E': (40, 59),
    'F': (0, 39)
}

# Grade assignment function
def get_grade(percentage):
    """Determine grade based on percentage"""
    for grade, (min_val, max_val) in GRADES.items():
        if min_val <= percentage <= max_val:
            return grade
    return 'F'

# Passing status threshold
PASS_THRESHOLD = 40

# Color palette for visualizations
CHART_COLORS = [
    'black', 'gray', 'silver', 'aqua', 'rosybrown', 'firebrick', 'red',
    'darksalmon', 'sienna', 'sandybrown', 'bisque', 'tan', 'snow', 'brown',
    'lightgray', 'lightcoral', 'maroon', 'mistyrose', 'coral', 'seashell',
    'peachpuff', 'darkorange', 'navajowhite', 'orange', 'darkgoldenrod',
    'lemonchiffon', 'ivory', 'olive', 'yellowgreen', 'lawngreen',
    'lightgreen', 'dimgray', 'darkgray', 'lightgrey', 'white', 'indianred',
    'darkred', 'salmon', 'orangered', 'chocolate', 'peru', 'burlywood',
    'blanchedalmond', 'wheat', 'goldenrod', 'khaki', 'beige', 'moccasin',
    'floralwhite', 'gold', 'darkkhaki'
]
