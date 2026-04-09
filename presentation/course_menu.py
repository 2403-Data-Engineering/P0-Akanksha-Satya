from service.course_service import CourseService


class CourseMenu:
    def __init__(self):
        self.service = CourseService()

    def display(self):
        while True:
            print("\n=== Course Menu ===")
            print("1. Add Course")
            print("2. View All Courses")
            print("3. Update Course")
            print("4. Remove Course")
            print("0. Back")

            choice = input("Choose: ")

            if choice == "1":
                self.add_course()
            elif choice == "2":
                self.view_courses()
            elif choice == "3":
                print("Update not implemented yet.")
            elif choice == "4":
                print("Delete not implemented yet.")
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def add_course(self):
        name = input("Course name: ")
        code = input("Course code: ")
        professor_id = input("Professor ID: ")

        print(self.service.add_course(name, code, professor_id))

    def view_courses(self):
        courses = self.service.get_all_courses()

        if not courses:
            print("No courses found.")
            return

        for course in courses:
            print(course)