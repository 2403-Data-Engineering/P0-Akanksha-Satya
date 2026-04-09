from data.db_connection import get_connection


class EnrollmentDAO:
    def enroll_student(self, student_id, course_id):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO enrollment (student_id, course_id)
        VALUES (%s, %s)
        """
        cursor.execute(query, (student_id, course_id))
        conn.commit()

        cursor.close()
        conn.close()

    def drop_student(self, student_id, course_id):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        DELETE FROM enrollment
        WHERE student_id = %s AND course_id = %s
        """
        cursor.execute(query, (student_id, course_id))
        conn.commit()

        cursor.close()
        conn.close()

    def get_students_in_course(self, course_id):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT student.id, student.first_name, student.last_name, student.email
        FROM enrollment
        JOIN student ON enrollment.student_id = student.id
        WHERE enrollment.course_id = %s
        """
        cursor.execute(query, (course_id,))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    def get_courses_for_student(self, student_id):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT course.id, course.course_name, course.course_code
        FROM enrollment
        JOIN course ON enrollment.course_id = course.id
        WHERE enrollment.student_id = %s
        """
        cursor.execute(query, (student_id,))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results