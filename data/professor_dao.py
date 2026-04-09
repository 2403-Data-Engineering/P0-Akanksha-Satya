from data.db_connection import get_connection


class ProfessorDAO:
    def add_professor(self, first, last, dept, email):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO professor (first_name, last_name, department, email)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (first, last, dept, email))
        conn.commit()

        cursor.close()
        conn.close()

    def get_all_professors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professor")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def get_professor_by_id(self, professor_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professor WHERE id = %s", (professor_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def get_professor_by_email(self, email):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professor WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def search_professors(self, query):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        SELECT * FROM professor
        WHERE CAST(id AS CHAR) LIKE %s
           OR first_name LIKE %s
           OR last_name LIKE %s
           OR department LIKE %s
           OR email LIKE %s
        """
        like_query = f"%{query}%"
        cursor.execute(sql, (like_query, like_query, like_query, like_query, like_query))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def update_professor(self, professor_id, first_name, last_name, department, email):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        UPDATE professor
        SET first_name = %s,
            last_name = %s,
            department = %s,
            email = %s
        WHERE id = %s
        """
        cursor.execute(query, (first_name, last_name, department, email, professor_id))
        conn.commit()
        cursor.close()
        conn.close()

    def remove_professor(self, professor_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM professor WHERE id = %s", (professor_id,))
        conn.commit()
        cursor.close()
        conn.close()