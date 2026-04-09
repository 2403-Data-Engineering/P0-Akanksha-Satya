from service.professor_service import ProfessorService


class ProfessorMenu:
    def __init__(self):
        self.service = ProfessorService()

    def display(self):
        while True:
            print("\n=== Professor Menu ===")
            print("1. Add Professor")
            print("2. View All Professors")
            print("3. Update Professor")
            print("4. Remove Professor")
            print("0. Back")

            choice = input("Choose: ")

            if choice == "1":
                self.add_professor()
            elif choice == "2":
                self.view_professors()
            elif choice == "3":
                print("Update not implemented yet.")
            elif choice == "4":
                print("Delete not implemented yet.")
            elif choice == "0":
                break

    def add_professor(self):
        first = input("First name: ")
        last = input("Last name: ")
        dept = input("Department: ")
        email = input("Email: ")

        result = self.service.add_professor(first, last, dept, email)
        print(result)

    def view_professors(self):
        professor = self.service.get_all_professors()

        if not professor:
            print("No professors found.")
            return

        for p in professor:
            print(p)