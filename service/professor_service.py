from data.professor_dao import ProfessorDAO
import mysql.connector


class ProfessorService:
    def __init__(self):
        self.dao = ProfessorDAO()

    def add_professor(self, first, last, dept, email):
        existing = self.dao.get_professor_by_email(email)
        if existing:
            return "A professor with this email already exists."

        self.dao.add_professor(first, last, dept, email)
        return "Professor added successfully."

    def get_all_professors(self):
        return self.dao.get_all_professors()

    def get_professor_by_id(self, professor_id):
        return self.dao.get_professor_by_id(professor_id)

    def search_professors(self, query):
        return self.dao.search_professors(query)

    def update_professor(self, professor_id, first_name, last_name, department, email):
        current = self.dao.get_professor_by_id(professor_id)
        existing = self.dao.get_professor_by_email(email)

        if existing and str(existing[0]) != str(professor_id):
            return "Another professor with this email already exists."

        self.dao.update_professor(professor_id, first_name, last_name, department, email)
        return "Professor profile updated successfully."

    def remove_professor(self, professor_id):
        try:
            self.dao.remove_professor(professor_id)
            return "Professor removed successfully."
        except mysql.connector.Error:
            return "Cannot remove professor. The professor may still be assigned to a course."