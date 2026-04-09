from data.course_dao import CourseDAO
import mysql.connector


class CourseService:
    def __init__(self):
        self.dao = CourseDAO()

    def add_course(self, course_name, course_code, professor_id):
        try:
            self.dao.add_course(course_name, course_code, professor_id)
            return "Course added successfully."
        except mysql.connector.Error as e:
            if e.errno == 1452:
                return "Error: Professor ID does not exist."
            return f"Database error: {e}"

    def get_all_courses(self):
        return self.dao.get_all_courses()

    def get_course_by_id(self, course_id):
        return self.dao.get_course_by_id(course_id)

    def get_courses_by_professor(self, professor_id):
        return self.dao.get_courses_by_professor(professor_id)

    def search_courses(self, query):
        return self.dao.search_courses(query)

    def unassign_professor_from_course(self, course_id):
        try:
            self.dao.unassign_professor_from_course(course_id)
            return "Professor removed from course successfully."
        except mysql.connector.Error as e:
            return f"Database error: {e}"

    def remove_course(self, course_id):
        try:
            self.dao.remove_course(course_id)
            return "Course removed successfully."
        except mysql.connector.Error:
            return "Cannot remove course. The course may still have enrollments."