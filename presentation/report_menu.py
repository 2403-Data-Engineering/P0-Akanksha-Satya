from service.report_service import ReportService


class ReportMenu:
    def __init__(self):
        self.service = ReportService()

    def display(self):
        while True:
            print("\n=== Revature Institute of Technology ===")
            print("=== Academic Advisor Portal ===")
            print("1. Open Advisor Home Page")
            print("2. View All Professors")
            print("3. View All Students")
            print("4. View All Courses")
            print("5. Generate Student Enrollment Report")
            print("6. Generate Professor Summary Report")
            print("0. Back")

            choice = input("Choose: ").strip()

            if choice == "1":
                print(self.service.generate_home_page())
            elif choice == "2":
                print(self.service.generate_all_professors_report())
            elif choice == "3":
                print(self.service.generate_all_students_report())
            elif choice == "4":
                print(self.service.generate_all_courses_report())
            elif choice == "5":
                student_id = input("Enter Student ID: ").strip()
                print(self.service.generate_student_enrollment_report(student_id))
            elif choice == "6":
                professor_id = input("Enter Professor ID: ").strip()
                print(self.service.generate_professor_summary_report(professor_id))
            elif choice == "0":
                break
            else:
                print("Invalid choice. Try again.")