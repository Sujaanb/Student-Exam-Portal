"""
Constants and configuration for the Student Examination Portal
"""

# File paths
STUDENT_FILE = 'Student.csv'
COURSE_FILE = 'Course.csv'
BATCH_FILE = 'Batch.csv'
DEPARTMENT_FILE = 'Department.csv'
EXAMINATION_FILE = 'Examination.csv'
RESULT_FILE = 'result.txt'

# CSV Headers
STUDENT_HEADERS = ['Student ID', 'Name', 'Class Roll No.', 'Batch ID']
COURSE_HEADERS = ['Course ID', 'Course Name', 'Marks Obtained']
BATCH_HEADERS = ['Batch ID', 'Batch Name', 'Department Name', 'List of Courses', 'List of Students']
DEPARTMENT_HEADERS = ['Department ID', 'Department Name', 'List of batches']
EXAMINATION_HEADERS = ['Examination ID', 'Course ID', 'Student ID', 'Marks', 'Date']

# Grade thresholds
GRADE_THRESHOLDS = {
    'A': 90,
    'B': 80,
    'C': 70,
    'D': 60,
    'E': 40,
    'F': 0
}

PASS_THRESHOLD = 40

# Delimiters for data relationships
STUDENT_COURSE_DELIMITER = '-'
STUDENT_COURSE_SEPARATOR = ':'
BATCH_LIST_DELIMITER = ':'
COURSE_LIST_DELIMITER = '-'

# Marks range
MIN_MARKS = 0
MAX_MARKS = 100

# Visualization
SCATTER_PLOT_COLORS = [
    'black', 'gray', 'silver', 'aqua', 'rosybrown', 'firebrick', 'red',
    'darksalmon', 'sienna', 'sandybrown', 'bisque', 'tan', 'snow', 'brown',
    'r', 'lightgray', 'W', 'lightcoral', 'maroon', 'mistyrose', 'coral',
    'seashell', 'peachpuff', 'darkorange', 'navajowhite', 'orange',
    'darkgoldenrod', 'lemonchiffon', 'Ivory', 'olive', 'yellowgreen',
    'lawngreen', 'lightgreen', 'dimgray', 'darkgray', 'lightgrey', 'white',
    'indianred', 'darkred', 'salmon', 'orangered', 'chocolate', 'peru',
    'burlywood', 'blanchedalmond', 'wheat', 'goldenrod', 'khaki', 'beige',
    'moccasin', 'floralwhite', 'gold', 'darkkhaki'
]

PIE_CHART_COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']

# Messages
ERROR_PREFIX = "❌ ERROR: "
SUCCESS_PREFIX = "✅ SUCCESS: "
INFO_PREFIX = "ℹ️ INFO: "
WARNING_PREFIX = "⚠️ WARNING: "

# Menu options
VALID_YES_RESPONSES = ('y', 'Y', 'yes', 'YES', 'Yes')
VALID_NO_RESPONSES = ('n', 'N', 'no', 'NO', 'No')

# Pagination
DEFAULT_PAGE_SIZE = 50
