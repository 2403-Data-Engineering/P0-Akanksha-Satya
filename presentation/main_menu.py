from presentation.professor_menu import ProfessorMenu
from presentation.student_menu import StudentMenu
from presentation.course_menu import CourseMenu
from presentation.enrollment_menu import EnrollmentMenu
from presentation.report_menu import ReportMenu


class MainMenu:
    def display(self):
        while True:
            print("\n=== College Administration System ===")
            print("1. Manage Professors")
            print("2. Manage Students")
            print("3. Manage Courses")
            print("4. Manage Enrollments")
            print("5. Academic Advisor Portal Reports")
            print("0. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                ProfessorMenu().display()
            elif choice == "2":
                StudentMenu().display()
            elif choice == "3":
                CourseMenu().display()
            elif choice == "4":
                EnrollmentMenu().display()
            elif choice == "5":
                ReportMenu().display()
            elif choice == "0":
                print("Exiting system.")
                break
            else:
                print("Invalid choice. Try again.")
