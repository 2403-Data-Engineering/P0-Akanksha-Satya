from data.student_dao import StudentDAO
import mysql.connector


class StudentService:
    def __init__(self):
        self.dao = StudentDAO()

    def add_student(self, first, last, email, major, year):
        existing = self.dao.get_student_by_email(email)
        if existing:
            return "A student with this email already exists."

        self.dao.add_student(first, last, email, major, year)
        return "Student added successfully."

    def get_all_students(self):
        return self.dao.get_all_students()

    def get_student_by_id(self, student_id):
        return self.dao.get_student_by_id(student_id)

    def search_students(self, query):
        return self.dao.search_students(query)

    def update_student(self, student_id, first_name, last_name, email, major, year):
        existing = self.dao.get_student_by_email(email)
        if existing and str(existing[0]) != str(student_id):
            return "Another student with this email already exists."

        self.dao.update_student(student_id, first_name, last_name, email, major, year)
        return "Student profile updated successfully."

    def remove_student(self, student_id):
        try:
            self.dao.remove_student(student_id)
            return "Student removed successfully."
        except mysql.connector.Error:
            return "Cannot remove student. The student may still be enrolled in a course."
