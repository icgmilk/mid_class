import sys
import json
import os

# File Paths
DATA_DIR = "data"
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")

# Date dictionary
DATE = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}

# credit limits
MAX_CREDITS = 25
MIN_CREDITS = 10

# Load Data
def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Create data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

students = load_data(STUDENTS_FILE)
courses = load_data(COURSES_FILE)

# Initialize Data if Empty
if not students:
    students = {
        "D1110176": {"name": "吳柏宏", "courses": ["001419", "001432", "001433", "001434", "001439", "228922", "383403"], "credits": 20},
        "D1123985": {"name": "許鈞翔", "courses": ["001419", "001432", "001433", "001434", "001439"], "credits": 15}
    }

if not courses:
    courses = {
        "001419": {"name": "作業系統", "credits": 3, "schedule": {'1' : [3, 4], '2' : [6]}},
        "001432": {"name": "軟體工程開發實務", "credits": 3, "schedule": {'3' : [6, 7, 8]}},
        "001433": {"name": "資料探勘導論", "credits": 3, "schedule": {'4' : [2, 3, 4]}},
        "001434": {"name": "資料科學實務", "credits": 3, "schedule": {'2' : [3, 4], '3' : [2]}},
        "001439": {"name": "編譯器", "credits": 3, "schedule": {'1' : [6], '3' : [3, 4]}},
        "065535": {"name": "普通物理(二)", "credits": 3, "schedule": {'5' : [1, 2, 3]}},
        "114514": {"name": "體育 - 空手道", "credits": 3, "schedule": {'5' : [6, 7, 8]}},
        "150449": {"name": "化妝品科學與應用", "credits": 3 , "schedule": {'3' : [7, 8, 9]}},
        "228922": {"name": "生命科學", "credits": 3 , "schedule": {'2' : [7, 8, 9]}},
        "383403": {"name": "微積分(一)", "credits": 4, "schedule": {'1' : [1, 2], '4' : [6, 7]}}
        
    }

# Utility Functions
def authenticate_student(student_id):
    if student_id in students:
        return True
    return False

def show_courses():
    for(course_id, course) in courses.items():
        print(f"{course_id} - {course['name']} ({course['credits']} credits)")
        print("Schedule:")
        for day, periods in course['schedule'].items():
            print(f"{DATE[int(day)]}: {', '.join([str(period) for period in periods])}")
        print()

def show_student_courses(student_id):
    course_ids = students[student_id]['courses']
    timetable = [dict() for _ in range(8)]
    for course_id in course_ids:
        for day, periods in courses[course_id]['schedule'].items():
            for time in periods:
                timetable[int(day)][time] = (course_id, courses[course_id]['name'])
    
    print('------------------------------')
    for day, schedule in enumerate(timetable[1:], start=1):
        print(f"{DATE[day]}:".rjust(12), end=' ')
        for time, (id, name) in sorted(schedule.items()):
            print(f"|{time} [{id}]{name}|", end=' ')
        print()
    print('------------------------------')
    print(f'current credits: {students[student_id]['credits']}')

def add_course(student_id, course_id):
    if course_id not in courses:
        print("\nError: Course does not exist.\n")
        return
    
    student = students[student_id]
    course = courses[course_id]

    if course_id in student['courses']:
        print(f"\nError: { student_id }({ student['name'] }) is already enrolled in this course.\n")
        return
    
    if student['credits'] + course['credits'] > MAX_CREDITS:
        print("\nError: Adding this course exceeds credit limit.\n")
        return
    
    def list_intersect(list1, list2):
        set1 = set(list1)
        for i in list2:
            if i in set1:
                return True
        return False
    
    for enrolled_course_id in student['courses']:
        for day, periods in courses[enrolled_course_id]['schedule'].items():
            if day in course['schedule'] and list_intersect(course['schedule'][day], periods):
                print("\nError: Course schedule conflicts with an already enrolled course.\n")
                return
    
    student['courses'].append(course_id)
    student['credits'] += course['credits']

    print(f"\nAdd Course { course['name'] }({ course_id }) Successful!\n")

def drop_course(student_id, course_id):
    
    student = students[student_id]
    if course_id == "":
        print("\nError: Course ID cannot be empty.\n")
        return
    
    if course_id not in student['courses']:
        print("\nError: Student is not enrolled in this course.\n")
        return
    
    if student['credits'] - courses[course_id]['credits'] < MIN_CREDITS:
        print("\nError: Dropping this course would go below the minimum credit limit.\n")
        return
    
    student['courses'].remove(course_id)
    student['credits'] -= courses[course_id]['credits']
    
    print(f"\nDrop Course { courses[course_id]['name'] }({ course_id }) Successful!\n")

def main():
    print("Welcome to the Feng Chia Course Selection System")
    student_id = input("Please enter your student ID: ")

    if not authenticate_student(student_id):
        print("Invalid student ID. Exiting.")
        sys.exit()
        
    while True:
        print("\n1. View Available Courses")
        print("2. View My Courses")
        print("3. Add Course")
        print("4. Drop Course")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            show_courses()
        elif choice == '2':
            show_student_courses(student_id)
        elif choice == '3':
            course_id = input("Please enter course ID you want to add: ")
            add_course(student_id, course_id)
        elif choice == '4':
            course_id = input("Please enter course ID you want to drop: ")
            drop_course(student_id, course_id)
        elif choice == '5':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    finally:
        save_data(STUDENTS_FILE, students)
        save_data(COURSES_FILE, courses)
