from data.enrollment_dao import EnrollmentDAO
import mysql.connector


class EnrollmentService:
    def __init__(self):
        self.dao = EnrollmentDAO()

    def enroll_student(self, student_id, course_id):
        try:
            self.dao.enroll_student(student_id, course_id)
            return "Student enrolled successfully."
        except mysql.connector.Error as e:
            if e.errno == 1452:
                return "Error: Student ID or Course ID does not exist."
            if e.errno == 1062:
                return "Error: Student is already enrolled in this course."
            return f"Database error: {e}"

    def drop_student(self, student_id, course_id):
        self.dao.drop_student(student_id, course_id)
        return "Student removed from course successfully."

    def get_students_in_course(self, course_id):
        return self.dao.get_students_in_course(course_id)

    def get_courses_for_student(self, student_id):
        return self.dao.get_courses_for_student(student_id)