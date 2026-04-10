from service.report_service import ReportService


class ReportMenu:
    def __init__(self):
        self.service = ReportService()

    def display(self):
        while True:
            print("\n=== Advisor Portal Reports ===")
            print("1. Open Student Enrollment Report")
            print("2. Open Professor Summary Report")
            print("0. Back")

            choice = input("Choose: ").strip()

            if choice == "1":
                student_id = input("Student ID: ").strip()
                if not student_id.isdigit():
                    print("Invalid ID. Please enter a number.")
                    continue
                print(self.service.open_student_report(student_id))
            elif choice == "2":
                professor_id = input("Professor ID: ").strip()
                if not professor_id.isdigit():
                    print("Invalid ID. Please enter a number.")
                    continue
                print(self.service.open_professor_report(professor_id))
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
