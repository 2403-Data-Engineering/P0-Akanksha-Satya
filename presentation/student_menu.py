from service.student_service import StudentService
from service.enrollment_service import EnrollmentService
from service.course_service import CourseService


class StudentMenu:
    def __init__(self):
        self.service = StudentService()
        self.enrollment_service = EnrollmentService()
        self.course_service = CourseService()

    def display(self):
        while True:
            print("\n=== Student Menu ===")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Students")
            print("4. Update Student")
            print("5. Remove Student")
            print("6. View Student Profile")
            print("7. Enroll Student in Course")
            print("8. Unenroll Student from Course")
            print("0. Back")

            choice = input("Choose: ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.search_students()
            elif choice == "4":
                self.update_student()
            elif choice == "5":
                self.remove_student()
            elif choice == "6":
                self.view_student_profile()
            elif choice == "7":
                self.enroll_student()
            elif choice == "8":
                self.unenroll_student()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def add_student(self):
        first = input("First name: ").strip()
        last = input("Last name: ").strip()
        email = input("Email: ").strip()
        major = input("Major: ").strip()
        year = input("Year: ").strip()
        print(self.service.add_student(first, last, email, major, year))

    def view_students(self):
        students = self.service.get_all_students()
        if not students:
            print("No students found.")
            return
        for s in students:
            print(s)

    def search_students(self):
        query = input("Search by ID, name, email, or major: ").strip()
        students = self.service.search_students(query)
        if not students:
            print("No matching students found.")
            return
        for s in students:
            print(s)

    def update_student(self):
        student_id = input("Student ID: ").strip()
        if not student_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        current = self.service.get_student_by_id(student_id)
        if not current:
            print("Student not found.")
            return

        print(f"Current student: {current}")
        first = input(f"First name [{current[1]}]: ").strip() or current[1]
        last = input(f"Last name [{current[2]}]: ").strip() or current[2]
        email = input(f"Email [{current[3]}]: ").strip() or current[3]
        major = input(f"Major [{current[4]}]: ").strip() or current[4]
        year = input(f"Year [{current[5]}]: ").strip() or current[5]

        print(self.service.update_student(student_id, first, last, email, major, year))

    def remove_student(self):
        student_id = input("Student ID to remove: ").strip()
        if not student_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        confirm = input("Are you sure? (y/n): ").strip().lower()
        if confirm != "y":
            print("Delete cancelled.")
            return

        print(self.service.remove_student(student_id))

    def view_student_profile(self):
        student_id = input("Student ID: ").strip()
        if not student_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        student = self.service.get_student_by_id(student_id)
        if not student:
            print("Student not found.")
            return

        print("\n=== Student Profile ===")
        print(f"ID: {student[0]}")
        print(f"Name: {student[1]} {student[2]}")
        print(f"Email: {student[3]}")
        print(f"Major: {student[4]}")
        print(f"Year: {student[5]}")
        print("\nEnrolled Courses:")

        courses = self.enrollment_service.get_courses_for_student(student_id)
        if not courses:
            print("No courses found.")
        else:
            for c in courses:
                print(c)

    def enroll_student(self):
        student_id = input("Student ID: ").strip()
        course_id = input("Course ID: ").strip()

        if not student_id.isdigit() or not course_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        print(self.enrollment_service.enroll_student(student_id, course_id))

    def unenroll_student(self):
        student_id = input("Student ID: ").strip()
        course_id = input("Course ID to drop: ").strip()

        if not student_id.isdigit() or not course_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        print(self.enrollment_service.drop_student(student_id, course_id))
