from service.enrollment_service import EnrollmentService


class EnrollmentMenu:
    def __init__(self):
        self.service = EnrollmentService()

    def display(self):
        while True:
            print("\n=== Enrollment Menu ===")
            print("1. Enroll Student in Course")
            print("2. Drop Student from Course")
            print("3. View Students in a Course")
            print("4. View Courses for a Student")
            print("0. Back")

            choice = input("Choose: ").strip()

            if choice == "1":
                self.enroll_student()
            elif choice == "2":
                self.drop_student()
            elif choice == "3":
                self.view_students_in_course()
            elif choice == "4":
                self.view_courses_for_student()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def enroll_student(self):
        student_id = input("Student ID: ").strip()
        course_id = input("Course ID: ").strip()

        if not student_id.isdigit() or not course_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        print(self.service.enroll_student(student_id, course_id))

    def drop_student(self):
        student_id = input("Student ID: ").strip()
        course_id = input("Course ID: ").strip()

        if not student_id.isdigit() or not course_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        print(self.service.drop_student(student_id, course_id))

    def view_students_in_course(self):
        course_id = input("Course ID: ").strip()
        if not course_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        students = self.service.get_students_in_course(course_id)
        if not students:
            print("No students enrolled in this course.")
            return

        for student in students:
            print(student)

    def view_courses_for_student(self):
        student_id = input("Student ID: ").strip()
        if not student_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        courses = self.service.get_courses_for_student(student_id)
        if not courses:
            print("This student is not enrolled in any courses.")
            return

        for course in courses:
            print(course)
