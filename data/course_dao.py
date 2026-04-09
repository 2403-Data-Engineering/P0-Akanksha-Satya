from data.db_connection import get_connection


class CourseDAO:
    def add_course(self, course_name, course_code, professor_id):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO course (course_name, course_code, professor_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (course_name, course_code, professor_id))
        conn.commit()

        cursor.close()
        conn.close()

    def get_all_courses(self):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT course.id, course.course_name, course.course_code,
               professor.first_name, professor.last_name
        FROM course
        JOIN professor ON course.professor_id = professor.id
        """
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        conn.close()
        return results

    def get_course_by_id(self, course_id):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT course.id, course.course_name, course.course_code, course.professor_id,
               professor.first_name, professor.last_name
        FROM course
        JOIN professor ON course.professor_id = professor.id
        WHERE course.id = %s
        """
        cursor.execute(query, (course_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def get_courses_by_professor(self, professor_id):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT id, course_name, course_code
        FROM course
        WHERE professor_id = %s
        """
        cursor.execute(query, (professor_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def search_courses(self, query):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        SELECT course.id, course.course_name, course.course_code,
               professor.first_name, professor.last_name
        FROM course
        JOIN professor ON course.professor_id = professor.id
        WHERE CAST(course.id AS CHAR) LIKE %s
           OR course.course_name LIKE %s
           OR course.course_code LIKE %s
           OR professor.first_name LIKE %s
           OR professor.last_name LIKE %s
        """
        like_query = f"%{query}%"
        cursor.execute(sql, (like_query, like_query, like_query, like_query, like_query))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def unassign_professor_from_course(self, course_id):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        UPDATE course
        SET professor_id = NULL
        WHERE id = %s
        """
        cursor.execute(query, (course_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def remove_course(self, course_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM course WHERE id = %s", (course_id,))
        conn.commit()
        cursor.close()
        conn.close()