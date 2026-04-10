from service.professor_service import ProfessorService
from service.course_service import CourseService


class ProfessorMenu:
    def __init__(self):
        self.service = ProfessorService()
        self.course_service = CourseService()

    def display(self):
        while True:
            print("\n=== Professor Menu ===")
            print("1. Add Professor")
            print("2. View All Professors")
            print("3. Search Professors")
            print("4. Update Professor")
            print("5. Remove Professor")
            print("6. View Professor Profile")
            print("7. Remove Professor from Course")
            print("0. Back")

            choice = input("Choose: ").strip()

            if choice == "1":
                self.add_professor()
            elif choice == "2":
                self.view_professors()
            elif choice == "3":
                self.search_professors()
            elif choice == "4":
                self.update_professor()
            elif choice == "5":
                self.remove_professor()
            elif choice == "6":
                self.view_professor_profile()
            elif choice == "7":
                self.unassign_from_course()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def add_professor(self):
        first = input("First name: ").strip()
        last = input("Last name: ").strip()
        dept = input("Department: ").strip()
        email = input("Email: ").strip()
        print(self.service.add_professor(first, last, dept, email))

    def view_professors(self):
        professors = self.service.get_all_professors()
        if not professors:
            print("No professors found.")
            return
        for p in professors:
            print(p)

    def search_professors(self):
        query = input("Search by ID, name, department, or email: ").strip()
        professors = self.service.search_professors(query)
        if not professors:
            print("No matching professors found.")
            return
        for p in professors:
            print(p)

    def update_professor(self):
        professor_id = input("Professor ID: ").strip()
        if not professor_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        current = self.service.get_professor_by_id(professor_id)
        if not current:
            print("Professor not found.")
            return

        print(f"Current professor: {current}")
        first = input(f"First name [{current[1]}]: ").strip() or current[1]
        last = input(f"Last name [{current[2]}]: ").strip() or current[2]
        dept = input(f"Department [{current[3]}]: ").strip() or current[3]
        email = input(f"Email [{current[4]}]: ").strip() or current[4]

        print(self.service.update_professor(professor_id, first, last, dept, email))

    def remove_professor(self):
        professor_id = input("Professor ID to remove: ").strip()
        if not professor_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        confirm = input("Are you sure? (y/n): ").strip().lower()
        if confirm != "y":
            print("Delete cancelled.")
            return

        print(self.service.remove_professor(professor_id))

    def view_professor_profile(self):
        professor_id = input("Professor ID: ").strip()
        if not professor_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        professor = self.service.get_professor_by_id(professor_id)
        if not professor:
            print("Professor not found.")
            return

        print("\n=== Professor Profile ===")
        print(f"ID: {professor[0]}")
        print(f"Name: {professor[1]} {professor[2]}")
        print(f"Department: {professor[3]}")
        print(f"Email: {professor[4]}")
        print("\nAssigned Courses:")

        courses = self.course_service.get_courses_by_professor(professor_id)
        if not courses:
            print("No courses assigned.")
        else:
            for c in courses:
                print(c)

    def unassign_from_course(self):
        professor_id = input("Professor ID: ").strip()
        course_id = input("Course ID: ").strip()

        if not professor_id.isdigit() or not course_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        print(self.course_service.unassign_professor_from_course(course_id))
