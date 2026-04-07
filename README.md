# Student Examination Portal

A comprehensive Python-based examination portal system for managing students, courses, batches, departments, and examination records.

## Features

### Core Functionality
- **Student Management** - Create, update, delete, and view student records
- **Course Management** - Manage courses, assign marks, and track performance
- **Batch Management** - Organize students into batches with course enrollment
- **Department Management** - Structure batches under departments
- **Examination Management** - Track and analyze exam performance
- **Report Card Generation** - Auto-calculate grades and generate report cards
- **Performance Analytics** - Visualize student performance with charts and statistics

### Advanced Features
- **Search Functionality** - Search students, courses, and batches by ID or name
- **Bulk Operations** - Import/export student and course data
- **Grade Distribution** - View grade statistics and pass/fail rates
- **Export Reports** - Generate detailed performance reports
- **Data Validation** - Input validation for all entries
- **Error Handling** - Comprehensive error handling and user-friendly messages

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Sujaanb/Student-Exam-Portal.git
cd Student-Exam-Portal
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python py_project/main.py
```

## Project Structure

```
Student-Exam-Portal/
├── py_project/
│   ├── main.py                 # Main entry point
│   ├── constants.py            # Application constants and configuration
│   ├── validators.py           # Input validation functions
│   ├── student.py              # Student management module
│   ├── course.py               # Course management module
│   ├── batch.py                # Batch management module
│   ├── department.py           # Department management module
│   ├── examination.py          # Examination management module
│   ├── utils.py                # Utility functions (helper functions)
│   ├── Student.csv             # Student records database
│   ├── Course.csv              # Course records database
│   ├── Batch.csv               # Batch records database
│   ├── Department.csv          # Department records database
│   └── Examination.csv         # Examination records database
├── requirements.txt            # Project dependencies
└── README.md                   # This file
```

## Usage

### Main Menu Options

1. **Student Details** - Manage student records
   - Create a new student
   - Update student details
   - Remove a student
   - Generate report card
   - Search for a student

2. **Course Details** - Manage courses
   - Create a new course
   - View student performance in course
   - Show course statistics
   - Search for a course

3. **Batch Details** - Manage batches
   - Create a new batch
   - View all students in batch
   - View all courses in batch
   - View batch performance analysis
   - View grade distribution pie chart

4. **Department Details** - Manage departments
   - Create a new department
   - View all batches in department
   - View average performance by batch
   - Show department statistics

5. **Examination Details** - View examination results
   - View overall student performance
   - Show examination statistics (scatter plot)

### Grading System

- **A**: 90-100%
- **B**: 80-89%
- **C**: 70-79%
- **D**: 60-69%
- **E**: 40-59%
- **F**: Below 40% (Fail)

## Data Format

### CSV Files
The system uses CSV files for data persistence:

- **Student.csv**: Student ID, Name, Class Roll No., Batch ID
- **Course.csv**: Course ID, Course Name, Marks Obtained
- **Batch.csv**: Batch ID, Batch Name, Department Name, List of Courses, List of Students
- **Department.csv**: Department ID, Department Name, List of Batches
- **Examination.csv**: Examination records

### Data Relationships

The system maintains relationships through delimited strings:
- Student-Course marks: `StudentID:Marks-StudentID:Marks-...`
- Department-Batch mapping: `BatchID:BatchID:...`
- Course-Student mapping: `StudentID:StudentID:...`

## Examples

### Creating a Student
```
1. Select "Student Details" from main menu
2. Choose "Create a new student"
3. Enter Student ID (unique identifier)
4. Enter Student Name
5. Enter Class Roll Number
6. Enter Batch ID (must exist)
7. Enter marks for each course in the batch
```

### Generating a Report Card
```
1. Select "Student Details" from main menu
2. Choose "Generate report card"
3. Enter the Student ID
4. View the generated report card with:
   - Student information
   - Percentage score
   - Overall grade
   - Pass/Fail status
```

### Viewing Batch Statistics
```
1. Select "Batch Details" from main menu
2. Choose "View complete performance of all students"
3. Enter Batch ID
4. View individual student performance for all courses
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid input formats
- Non-existent IDs
- File operation errors
- Data validation failures
- Duplicate entries

All errors display user-friendly messages with guidance on how to proceed.

## Performance Features

### Search Functionality
- Search students by ID or name
- Search courses by ID or name
- Search batches by ID or name

### Analytics
- Calculate average marks per student
- Calculate average marks per course
- Generate grade distribution statistics
- Visualize performance with scatter plots
- Generate pie charts for grade distribution

### Export & Reports
- Generate text-based report cards
- Export grade distributions
- Create performance summaries

## Future Enhancements

- [ ] Migration to SQLite/PostgreSQL database
- [ ] Web interface with Flask/Django
- [ ] PDF report generation
- [ ] Advanced analytics dashboards
- [ ] User authentication system
- [ ] Email notifications
- [ ] Mobile app support

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -am 'Add improvement'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

## Author

Created by [Sujaan Bhattacharyya](https://github.com/Sujaanb)

---

**Last Updated:** 2024
**Version:** 2.0 (Improved with modular architecture)
