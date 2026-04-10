from service.course_service import CourseService
from service.enrollment_service import EnrollmentService
from service.student_service import StudentService
from service.professor_service import ProfessorService


class CourseMenu:
    def __init__(self):
        self.service = CourseService()
        self.enrollment_service = EnrollmentService()
        self.student_service = StudentService()
        self.professor_service = ProfessorService()

    def display(self):
        while True:
            print("\n=== Course Menu ===")
            print("1. Add Course")
            print("2. View All Courses")
            print("3. Search Courses")
            print("4. Remove Course")
            print("5. View Course Profile")
            print("6. Add Student to Course")
            print("0. Back")

            choice = input("Choose: ").strip()

            if choice == "1":
                self.add_course()
            elif choice == "2":
                self.view_courses()
            elif choice == "3":
                self.search_courses()
            elif choice == "4":
                self.remove_course()
            elif choice == "5":
                self.view_course_profile()
            elif choice == "6":
                self.add_student_to_course()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def add_course(self):
        course_name = input("Course name: ").strip()
        course_code = input("Course code: ").strip()
        professor_id = input("Professor ID: ").strip()

        if not professor_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        print(self.service.add_course(course_name, course_code, professor_id))

    def view_courses(self):
        courses = self.service.get_all_courses()
        if not courses:
            print("No courses found.")
            return
        for c in courses:
            print(c)

    def search_courses(self):
        query = input("Search by ID, course name, code, or professor: ").strip()
        courses = self.service.search_courses(query)
        if not courses:
            print("No matching courses found.")
            return
        for c in courses:
            print(c)

    def remove_course(self):
        course_id = input("Course ID to remove: ").strip()
        if not course_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        confirm = input("Are you sure? (y/n): ").strip().lower()
        if confirm != "y":
            print("Delete cancelled.")
            return

        print(self.service.remove_course(course_id))

    def view_course_profile(self):
        course_id = input("Course ID: ").strip()
        if not course_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        course = self.service.get_course_by_id(course_id)
        if not course:
            print("Course not found.")
            return

        print("\n=== Course Profile ===")
        print(f"ID: {course[0]}")
        print(f"Course Name: {course[1]}")
        print(f"Course Code: {course[2]}")
        print(f"Professor ID: {course[3]}")
        print(f"Professor: {course[4]} {course[5]}")
        print("\nStudents in Course:")

        students = self.enrollment_service.get_students_in_course(course_id)
        if not students:
            print("No students enrolled.")
        else:
            for s in students:
                print(s)

    def add_student_to_course(self):
        course_id = input("Course ID: ").strip()
        student_id = input("Student ID: ").strip()

        if not course_id.isdigit() or not student_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        print(self.enrollment_service.enroll_student(student_id, course_id))
