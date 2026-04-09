from data.db_connection import get_connection


class StudentDAO:
    def add_student(self, first, last, email, major, year):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO student (first_name, last_name, email, major, year)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first, last, email, major, year))
        conn.commit()

        cursor.close()
        conn.close()

    def get_all_students(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def get_student_by_id(self, student_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def search_students(self, query):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        SELECT * FROM student
        WHERE CAST(id AS CHAR) LIKE %s
           OR first_name LIKE %s
           OR last_name LIKE %s
           OR email LIKE %s
           OR major LIKE %s
        """
        like_query = f"%{query}%"
        cursor.execute(sql, (like_query, like_query, like_query, like_query, like_query))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def update_student(self, student_id, first_name, last_name, email, major, year):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        UPDATE student
        SET first_name = %s,
            last_name = %s,
            email = %s,
            major = %s,
            year = %s
        WHERE id = %s
        """
        cursor.execute(query, (first_name, last_name, email, major, year, student_id))
        conn.commit()
        cursor.close()
        conn.close()

    def remove_student(self, student_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE id = %s", (student_id,))
        conn.commit()
        cursor.close()
        conn.close()
    def get_student_by_email(self, email):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result