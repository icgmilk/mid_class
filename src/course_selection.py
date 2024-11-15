import sys
import json
import os

# File Paths
DATA_DIR = "data"
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")

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

# Date directory

date = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}

# Create data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

students = load_data(STUDENTS_FILE)
courses = load_data(COURSES_FILE)

# Initialize Data if Empty
if not students:
    students = {
        "D1110176": {"name": "吳柏宏", "courses": [], "credits": 0},
        "D1123985": {"name": "許鈞翔", "courses": [], "credits": 0}
    }
    save_data(STUDENTS_FILE, students)

if not courses:
    courses = {
        "001419": {"name": "作業系統", "credits": 3, "schedule": {1 : [3, 4], 2 : [6]}},
        "001432": {"name": "軟體工程開發實務", "credits": 3, "schedule": {3 : [6, 7, 8]}},
        "001434": {"name": "資料科學實務", "credits": 3, "schedule": {2 : [3, 4], 3 : [2]}},
        "001433": {"name": "資料探勘導論", "credits": 3, "schedule": {4 : [2, 3, 4]}},
        "001439": {"name": "編譯器", "credits": 3, "schedule": {1 : [6], 3 : [3, 4]}},
        "114514": {"name": "體育 - 空手道", "credits": 3, "schedule": {5 : [6, 7, 8]}},
        "150449": {"name": "化妝品科學與應用", "credits": 3 , "schedule": {3 : [7, 8, 9]}},
        "228922": {"name": "生命科學", "credits": 3 , "schedule": {2 : [7, 8, 9]}},
        "383403": {"name": "微積分(一)", "credits": 4, "schedule": {1 : [1, 2], 4 : [6, 7]}},
        "065535": {"name": "普通物理(二)", "credits": 3, "schedule": {5 : [1, 2, 3]}}
    }
    save_data(COURSES_FILE, courses)

# Utility Functions
def authenticate_student(student_id):
    if student_id in students:
        return True
    return False

def show_courses():
    global date
    for(course_id, course) in courses.items():
        print(f"{course_id} - {course['name']} ({course['credits']} credits)")
        print("Schedule:")
        for day, periods in course['schedule'].items():
            print(f"{date[int(day)]}: {', '.join([str(period) for period in periods])}")
        print()

def show_student_courses(student_id):
    pass

def add_course(student_id, course_id):
    pass

def drop_course(student_id, course_id):
    pass

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
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
