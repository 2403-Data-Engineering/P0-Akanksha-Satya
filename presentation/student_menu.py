from service.student_service import StudentService


class StudentMenu:
    def __init__(self):
        self.service = StudentService()

    def display(self):
        while True:
            print("\n=== Student Menu ===")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Update Student")
            print("4. Remove Student")
            print("0. Back")

            choice = input("Choose: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                print("Update not implemented yet.")
            elif choice == "4":
                print("Delete not implemented yet.")
            elif choice == "0":
                break
            else:
                print("Invalid choice. Try again.")

    def add_student(self):
        first = input("First name: ")
        last = input("Last name: ")
        email = input("Email: ")
        major = input("Major: ")
        year = input("Year: ")

        print(self.service.add_student(first, last, email, major, year))

    def view_students(self):
        students = self.service.get_all_students()

        if not students:
            print("No students found.")
            return

        for student in students:
            print(student)