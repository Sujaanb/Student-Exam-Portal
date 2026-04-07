# Student Examination Portal - Main Application
# Improved version with fixes, error handling, and modular utilities

import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from config import FILES, PASS_THRESHOLD, get_grade, CHART_COLORS
from utils import (
    read_csv, check_id_exists, get_valid_marks, get_valid_input,
    parse_marks_string, calculate_percentage, get_passing_status,
    help1, help2, generate_report_card, initialize_csv_files, csv_file_exists
)

# Initialize CSV files on startup
initialize_csv_files()

def student():
    """Student module - Create, Update, Remove, and Generate Reports"""
    while True:
        print('\n--- STUDENT MENU ---')
        print('a. Create a new student')
        print('b. Update student details')
        print('c. Remove a student from the database')
        print('d. Generate report card')
        print('e. Exit')
        ch1 = input('Enter your choice: ').strip()
        
        if ch1.lower() == 'a':
            while True:
                try:
                    student_id = input('Enter Student ID: ').strip()
                    
                    # Check if student already exists
                    if check_id_exists(FILES['STUDENT'], 0, student_id):
                        print('Error: This student already exists')
                        continue
                    
                    name = input('Enter name of the Student: ').strip()
                    roll_no = input('Enter class roll number: ').strip()
                    batch_id = input('Enter Batch ID: ').strip()
                    
                    # Verify batch exists
                    if not check_id_exists(FILES['BATCH'], 0, batch_id):
                        print('Error: This batch does not exist')
                        print('Note: A student can only be enrolled in an existing batch!')
                        continue
                    
                    # Add student to Student.csv
                    try:
                        with open(FILES['STUDENT'], 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow([student_id, name, roll_no, batch_id])
                        
                        # Update Batch.csv with student
                        df_batch = pd.read_csv(FILES['BATCH'])
                        batch_idx = df_batch[df_batch['Batch ID'] == batch_id].index[0]
                        current_students = df_batch.loc[batch_idx, 'List of Students']
                        new_students = current_students + ':' + student_id if current_students else student_id
                        df_batch.loc[batch_idx, 'List of Students'] = new_students
                        df_batch.to_csv(FILES['BATCH'], index=False)
                        
                        # Get courses for this batch and add marks entries
                        courses = df_batch.loc[batch_idx, 'List of Courses'].split(':')
                        for course_id in courses:
                            if course_id.strip():
                                df_course = pd.read_csv(FILES['COURSE'])
                                course_idx = df_course[df_course['Course ID'] == course_id].index[0]
                                marks = get_valid_marks(f'Enter marks for course {course_id}: ')
                                current_marks = df_course.loc[course_idx, 'Marks Obtained']
                                new_marks = current_marks + '-' + student_id + ':' + str(marks) if current_marks else student_id + ':' + str(marks)
                                df_course.loc[course_idx, 'Marks Obtained'] = new_marks
                                df_course.to_csv(FILES['COURSE'], index=False)
                        
                        print(f'Student {student_id} created successfully!')
                    
                    except Exception as e:
                        print(f'Error adding student: {e}')
                        continue
                    
                    repeat = input('Enter more students? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch1.lower() == 'b':
            while True:
                try:
                    student_id = input('Enter Student ID to update: ').strip()
                    
                    if not check_id_exists(FILES['STUDENT'], 0, student_id):
                        print('Error: This student does not exist')
                        continue
                    
                    name = input('Enter new name: ').strip()
                    roll_no = input('Enter new class roll number: ').strip()
                    
                    df = pd.read_csv(FILES['STUDENT'])
                    idx = df[df['Student ID'] == student_id].index[0]
                    df.loc[idx, 'Name'] = name
                    df.loc[idx, 'Class Roll No.'] = roll_no
                    df.to_csv(FILES['STUDENT'], index=False)
                    
                    print('Student updated successfully!')
                    
                    repeat = input('Update more students? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch1.lower() == 'c':
            while True:
                try:
                    student_id = input('Enter Student ID to delete: ').strip()
                    
                    if not check_id_exists(FILES['STUDENT'], 0, student_id):
                        print('Error: This student does not exist')
                        continue
                    
                    # Remove from Student.csv
                    df_student = pd.read_csv(FILES['STUDENT'])
                    batch_id = df_student[df_student['Student ID'] == student_id]['Batch ID'].values[0]
                    df_student = df_student[df_student['Student ID'] != student_id]
                    df_student.to_csv(FILES['STUDENT'], index=False)
                    
                    # Remove from Batch.csv
                    df_batch = pd.read_csv(FILES['BATCH'])
                    batch_idx = df_batch[df_batch['Batch ID'] == batch_id].index[0]
                    students = df_batch.loc[batch_idx, 'List of Students']
                    students = students.replace(':' + student_id, '').replace(student_id + ':', '').replace(student_id, '')
                    df_batch.loc[batch_idx, 'List of Students'] = students
                    df_batch.to_csv(FILES['BATCH'], index=False)
                    
                    # Remove from Course.csv
                    df_course = pd.read_csv(FILES['COURSE'])
                    for idx, row in df_course.iterrows():
                        if student_id in str(row['Marks Obtained']):
                            marks = row['Marks Obtained']
                            marks = marks.replace('-' + student_id + ':', '').replace(student_id + ':', '')
                            df_course.loc[idx, 'Marks Obtained'] = marks
                    df_course.to_csv(FILES['COURSE'], index=False)
                    
                    print('Student deleted successfully!')
                    
                    repeat = input('Delete more students? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch1.lower() == 'd':
            while True:
                try:
                    student_id = input('Enter Student ID for report: ').strip()
                    
                    df_student = pd.read_csv(FILES['STUDENT'])
                    if student_id not in df_student['Student ID'].values:
                        print('Error: This student does not exist')
                        continue
                    
                    # Get student info
                    student_info = df_student[df_student['Student ID'] == student_id].iloc[0]
                    name = student_info['Name']
                    roll_no = student_info['Class Roll No.']
                    batch_id = student_info['Batch ID']
                    
                    # Get courses for batch
                    df_batch = pd.read_csv(FILES['BATCH'])
                    courses = df_batch[df_batch['Batch ID'] == batch_id]['List of Courses'].values[0].split(':')
                    
                    # Calculate percentage
                    total_marks = 0
                    valid_courses = 0
                    df_course = pd.read_csv(FILES['COURSE'])
                    
                    for course_id in courses:
                        if course_id.strip():
                            course_row = df_course[df_course['Course ID'] == course_id]
                            if not course_row.empty:
                                marks_str = course_row.iloc[0]['Marks Obtained']
                                marks = parse_marks_string(marks_str, student_id)
                                if marks > 0:
                                    total_marks += marks
                                    valid_courses += 1
                    
                    percentage = (total_marks / valid_courses) if valid_courses > 0 else 0
                    grade = get_grade(percentage)
                    status = get_passing_status(percentage)
                    
                    generate_report_card(student_id, name, roll_no, batch_id, percentage, grade, status)
                    
                    repeat = input('Generate more reports? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch1.lower() == 'e':
            break
        else:
            print('Invalid input!')


def course():
    """Course module - Create courses and view performance"""
    while True:
        print('\n--- COURSE MENU ---')
        print('a. Create a new course')
        print('b. View performance of all students in the course')
        print('c. Exit')
        ch2 = input('Enter your choice: ').strip()
        
        if ch2.lower() == 'a':
            while True:
                try:
                    course_id = input('Enter Course ID: ').strip()
                    
                    if check_id_exists(FILES['COURSE'], 0, course_id):
                        print('Error: This course already exists')
                        continue
                    
                    course_name = input('Enter Course Name: ').strip()
                    batch_id = input('Enter Batch ID: ').strip()
                    
                    if not check_id_exists(FILES['BATCH'], 0, batch_id):
                        print('Error: This batch does not exist')
                        continue
                    
                    # Get students in batch
                    df_batch = pd.read_csv(FILES['BATCH'])
                    students = df_batch[df_batch['Batch ID'] == batch_id]['List of Students'].values[0].split(':')
                    students = [s.strip() for s in students if s.strip()]
                    
                    # Get marks for each student
                    marks_entries = []
                    for student_id in students:
                        marks = get_valid_marks(f'Enter marks for student {student_id}: ')
                        marks_entries.append(f'{student_id}:{marks}')
                    
                    marks_str = '-'.join(marks_entries)
                    student_str = ':'.join(students)
                    
                    # Add to Course.csv
                    with open(FILES['COURSE'], 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([course_id, course_name, marks_str])
                    
                    # Update Batch.csv
                    df_batch = pd.read_csv(FILES['BATCH'])
                    batch_idx = df_batch[df_batch['Batch ID'] == batch_id].index[0]
                    current_courses = df_batch.loc[batch_idx, 'List of Courses']
                    new_courses = current_courses + ':' + course_id if current_courses else course_id
                    df_batch.loc[batch_idx, 'List of Courses'] = new_courses
                    df_batch.to_csv(FILES['BATCH'], index=False)
                    
                    print('Course created successfully!')
                    
                    repeat = input('Add more courses? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch2.lower() == 'b':
            while True:
                try:
                    course_id = input('Enter Course ID: ').strip()
                    df_course = pd.read_csv(FILES['COURSE'])
                    
                    if course_id not in df_course['Course ID'].values:
                        print('Error: This course does not exist')
                        continue
                    
                    course_row = df_course[df_course['Course ID'] == course_id].iloc[0]
                    marks_str = course_row['Marks Obtained']
                    
                    print(f'\n--- Performance in Course {course_id} ---')
                    entries = marks_str.split('-')
                    for entry in entries:
                        if ':' in entry:
                            student_id, marks = entry.split(':')
                            df_student = pd.read_csv(FILES['STUDENT'])
                            student_row = df_student[df_student['Student ID'] == student_id.strip()]
                            if not student_row.empty:
                                print(f'Student ID: {student_id}')
                                print(f'Name: {student_row.iloc[0]["Name"]}')
                                print(f'Marks: {marks}')
                                print()
                    
                    repeat = input('Check another course? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch2.lower() == 'c':
            break
        else:
            print('Invalid input!')


def batch():
    """Batch module - Create batches and view batch information"""
    while True:
        print('\n--- BATCH MENU ---')
        print('a. Create a new batch')
        print('b. View list of all students in a batch')
        print('c. View list of all courses taught in the batch')
        print('d. View complete performance of all students in a batch')
        print('e. Pie chart of percentage of all students')
        print('f. Exit')
        ch3 = input('Enter your choice: ').strip()
        
        if ch3.lower() == 'a':
            while True:
                try:
                    batch_id = input('Enter Batch ID: ').strip()
                    
                    if check_id_exists(FILES['BATCH'], 0, batch_id):
                        print('Error: This batch already exists')
                        continue
                    
                    batch_name = input('Enter Batch Name: ').strip()
                    dept_name = input('Enter Department Name: ').strip()
                    
                    if not check_id_exists(FILES['DEPARTMENT'], 1, dept_name):
                        print('Error: This department does not exist')
                        continue
                    
                    # Add batch
                    with open(FILES['BATCH'], 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([batch_id, batch_name, dept_name, '', ''])
                    
                    # Update Department.csv
                    df_dept = pd.read_csv(FILES['DEPARTMENT'])
                    dept_idx = df_dept[df_dept['Department Name'] == dept_name].index[0]
                    current_batches = df_dept.loc[dept_idx, 'List of batches']
                    new_batches = current_batches + ':' + batch_id if current_batches else batch_id
                    df_dept.loc[dept_idx, 'List of batches'] = new_batches
                    df_dept.to_csv(FILES['DEPARTMENT'], index=False)
                    
                    print('Batch created successfully!')
                    
                    repeat = input('Create more batches? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch3.lower() == 'b':
            while True:
                try:
                    batch_id = input('Enter Batch ID: ').strip()
                    df_student = pd.read_csv(FILES['STUDENT'])
                    students = df_student[df_student['Batch ID'] == batch_id]
                    
                    if students.empty:
                        print('No students in this batch')
                    else:
                        print(f'\n--- Students in Batch {batch_id} ---')
                        for _, row in students.iterrows():
                            print(f'Student ID: {row["Student ID"]}')
                            print(f'Name: {row["Name"]}')
                            print()
                    
                    repeat = input('Check another batch? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch3.lower() == 'c':
            while True:
                try:
                    batch_id = input('Enter Batch ID: ').strip()
                    df_batch = pd.read_csv(FILES['BATCH'])
                    
                    if batch_id not in df_batch['Batch ID'].values:
                        print('Error: This batch does not exist')
                        continue
                    
                    courses = df_batch[df_batch['Batch ID'] == batch_id]['List of Courses'].values[0]
                    print(f'\n--- Courses in Batch {batch_id} ---')
                    if courses:
                        for course in courses.split(':'):
                            if course.strip():
                                print(course.strip())
                    else:
                        print('No courses in this batch')
                    
                    repeat = input('Check another batch? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch3.lower() == 'd':
            while True:
                try:
                    batch_id = input('Enter Batch ID: ').strip()
                    
                    df_batch = pd.read_csv(FILES['BATCH'])
                    if batch_id not in df_batch['Batch ID'].values:
                        print('Error: This batch does not exist')
                        continue
                    
                    courses = df_batch[df_batch['Batch ID'] == batch_id]['List of Courses'].values[0].split(':')
                    df_student = pd.read_csv(FILES['STUDENT'])
                    students = df_student[df_student['Batch ID'] == batch_id]
                    
                    print(f'\n--- Performance Report for Batch {batch_id} ---')
                    for _, student_row in students.iterrows():
                        student_id = student_row['Student ID']
                        total_marks = 0
                        valid_courses = 0
                        
                        df_course = pd.read_csv(FILES['COURSE'])
                        for course_id in courses:
                            if course_id.strip():
                                course_row = df_course[df_course['Course ID'] == course_id]
                                if not course_row.empty:
                                    marks_str = course_row.iloc[0]['Marks Obtained']
                                    marks = parse_marks_string(marks_str, student_id)
                                    if marks > 0:
                                        total_marks += marks
                                        valid_courses += 1
                        
                        percentage = (total_marks / valid_courses) if valid_courses > 0 else 0
                        print(f'Student ID: {student_id}, Name: {student_row["Name"]}, Percentage: {percentage:.2f}%')
                    
                    repeat = input('Check another batch? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch3.lower() == 'e':
            try:
                batch_id = input('Enter Batch ID: ').strip()
                
                df_batch = pd.read_csv(FILES['BATCH'])
                if batch_id not in df_batch['Batch ID'].values:
                    print('Error: This batch does not exist')
                    continue
                
                courses = df_batch[df_batch['Batch ID'] == batch_id]['List of Courses'].values[0].split(':')
                df_student = pd.read_csv(FILES['STUDENT'])
                students = df_student[df_student['Batch ID'] == batch_id]
                
                percentages = []
                student_names = []
                
                for _, student_row in students.iterrows():
                    student_id = student_row['Student ID']
                    total_marks = 0
                    valid_courses = 0
                    
                    df_course = pd.read_csv(FILES['COURSE'])
                    for course_id in courses:
                        if course_id.strip():
                            course_row = df_course[df_course['Course ID'] == course_id]
                            if not course_row.empty:
                                marks_str = course_row.iloc[0]['Marks Obtained']
                                marks = parse_marks_string(marks_str, student_id)
                                if marks > 0:
                                    total_marks += marks
                                    valid_courses += 1
                    
                    percentage = (total_marks / valid_courses) if valid_courses > 0 else 0
                    percentages.append(percentage)
                    student_names.append(student_id)
                
                # Create pie chart
                colors = CHART_COLORS[:len(percentages)]
                plt.figure(figsize=(10, 6))
                plt.pie(percentages, labels=student_names, colors=colors, autopct='%1.1f%%')
                plt.title(f'Student Performance Distribution - Batch {batch_id}')
                plt.show()
            
            except Exception as e:
                print(f'Error: {e}')
        
        elif ch3.lower() == 'f':
            break
        else:
            print('Invalid input!')


def dept():
    """Department module - Create departments and view department information"""
    while True:
        print('\n--- DEPARTMENT MENU ---')
        print('a. Create a new Department')
        print('b. View all batches in a department')
        print('c. View average performance of all batches in a department')
        print('d. Exit')
        ch4 = input('Enter your choice: ').strip()
        
        if ch4.lower() == 'a':
            while True:
                try:
                    dept_id = input('Enter Department ID: ').strip()
                    
                    if check_id_exists(FILES['DEPARTMENT'], 0, dept_id):
                        print('Error: This department already exists')
                        continue
                    
                    dept_name = input('Enter Department Name: ').strip()
                    
                    with open(FILES['DEPARTMENT'], 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([dept_id, dept_name, ''])
                    
                    print('Department created successfully!')
                    
                    repeat = input('Create more departments? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch4.lower() == 'b':
            while True:
                try:
                    dept_id = input('Enter Department ID: ').strip()
                    df_dept = pd.read_csv(FILES['DEPARTMENT'])
                    
                    if dept_id not in df_dept['Department ID'].values:
                        print('Error: This department does not exist')
                        continue
                    
                    batches = df_dept[df_dept['Department ID'] == dept_id]['List of batches'].values[0]
                    print(f'\n--- Batches in Department {dept_id} ---')
                    if batches:
                        for batch in batches.split(':'):
                            if batch.strip():
                                print(batch.strip())
                    else:
                        print('No batches in this department')
                    
                    repeat = input('Check another department? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch4.lower() == 'c':
            while True:
                try:
                    dept_id = input('Enter Department ID: ').strip()
                    df_dept = pd.read_csv(FILES['DEPARTMENT'])
                    
                    if dept_id not in df_dept['Department ID'].values:
                        print('Error: This department does not exist')
                        continue
                    
                    batches_str = df_dept[df_dept['Department ID'] == dept_id]['List of batches'].values[0]
                    batches = [b.strip() for b in batches_str.split(':') if b.strip()]
                    
                    print(f'\n--- Average Performance for Department {dept_id} ---')
                    for batch_id in batches:
                        df_batch = pd.read_csv(FILES['BATCH'])
                        courses = df_batch[df_batch['Batch ID'] == batch_id]['List of Courses'].values[0].split(':')
                        
                        df_student = pd.read_csv(FILES['STUDENT'])
                        students = df_student[df_student['Batch ID'] == batch_id]
                        
                        total_percentage = 0
                        student_count = 0
                        
                        for _, student_row in students.iterrows():
                            student_id = student_row['Student ID']
                            total_marks = 0
                            valid_courses = 0
                            
                            df_course = pd.read_csv(FILES['COURSE'])
                            for course_id in courses:
                                if course_id.strip():
                                    course_row = df_course[df_course['Course ID'] == course_id]
                                    if not course_row.empty:
                                        marks_str = course_row.iloc[0]['Marks Obtained']
                                        marks = parse_marks_string(marks_str, student_id)
                                        if marks > 0:
                                            total_marks += marks
                                            valid_courses += 1
                            
                            percentage = (total_marks / valid_courses) if valid_courses > 0 else 0
                            total_percentage += percentage
                            student_count += 1
                        
                        avg_percentage = (total_percentage / student_count) if student_count > 0 else 0
                        print(f'Batch ID: {batch_id}, Average Percentage: {avg_percentage:.2f}%')
                    
                    repeat = input('Check another department? (y/n): ').strip().lower()
                    if repeat != 'y':
                        break
                
                except Exception as e:
                    print(f'Error: {e}')
                    continue
        
        elif ch4.lower() == 'd':
            break
        else:
            print('Invalid input!')


def exam():
    """Examination module - View exam statistics and performance"""
    while True:
        print('\n--- EXAMINATION MENU ---')
        print('a. View performance of all students')
        print('b. Scatter plot of all marks obtained')
        print('c. Exit')
        ch5 = input('Enter your choice: ').strip()
        
        if ch5.lower() == 'a':
            try:
                df_student = pd.read_csv(FILES['STUDENT'])
                df_course = pd.read_csv(FILES['COURSE'])
                
                print('\n--- Overall Student Performance ---')
                for _, student_row in df_student.iterrows():
                    student_id = student_row['Student ID']
                    marks_list = []
                    
                    for _, course_row in df_course.iterrows():
                        marks = parse_marks_string(course_row['Marks Obtained'], student_id)
                        if marks > 0:
                            marks_list.append(marks)
                    
                    if marks_list:
                        avg_percentage = calculate_percentage(marks_list)
                        print(f'Student ID: {student_id}, Overall Percentage: {avg_percentage:.2f}%')
            
            except Exception as e:
                print(f'Error: {e}')
        
        elif ch5.lower() == 'b':
            try:
                df_course = pd.read_csv(FILES['COURSE'])
                course_ids = []
                marks_list = []
                
                for _, course_row in df_course.iterrows():
                    if course_row['Marks Obtained'] != 'Marks Obtained':
                        course_ids.append(course_row['Course ID'])
                        marks_str = course_row['Marks Obtained']
                        course_marks = []
                        
                        entries = marks_str.split('-')
                        for entry in entries:
                            if ':' in entry:
                                _, marks = entry.split(':')
                                if marks.isdigit():
                                    course_marks.append(int(marks))
                        
                        marks_list.append(course_marks)
                
                colors = CHART_COLORS[:len(course_ids)]
                plt.figure(figsize=(10, 6))
                
                for i, course_id in enumerate(course_ids):
                    avg_marks = sum(marks_list[i]) / len(marks_list[i]) if marks_list[i] else 0
                    plt.scatter(avg_marks, course_id, c=colors[i], s=100)
                
                plt.xlabel('Average Marks')
                plt.ylabel('Course ID')
                plt.title('Course-wise Performance Distribution')
                plt.show()
            
            except Exception as e:
                print(f'Error: {e}')
        
        elif ch5.lower() == 'c':
            break
        else:
            print('Invalid input!')


def main():
    """Main application loop"""
    while True:
        print('\n' + '='*50)
        print('STUDENT EXAMINATION PORTAL')
        print('='*50)
        print('1. Student Details')
        print('2. Course Details')
        print('3. Batch Details')
        print('4. Department Details')
        print('5. Examination Details')
        print('6. Exit')
        print('='*50)
        
        try:
            ch = input('Enter your choice: ').strip()
            
            if ch == '1':
                student()
            elif ch == '2':
                course()
            elif ch == '3':
                batch()
            elif ch == '4':
                dept()
            elif ch == '5':
                exam()
            elif ch == '6':
                print('Thank you for using Student Examination Portal!')
                break
            else:
                print('Invalid input! Please try again.')
        
        except KeyboardInterrupt:
            print('\n\nProgram interrupted by user')
            break
        except Exception as e:
            print(f'Error: {e}')


if __name__ == '__main__':
    main()
