import webbrowser
from reports.report_helper import (
    html_page,
    build_html_table,
    build_markdown_table,
    write_file
)
from data.professor_dao import ProfessorDAO
from data.student_dao import StudentDAO
from data.course_dao import CourseDAO
from data.enrollment_dao import EnrollmentDAO
from data.db_connection import get_connection


class AdvisorPortal:
    def __init__(self):
        self.professor_dao = ProfessorDAO()
        self.student_dao = StudentDAO()
        self.course_dao = CourseDAO()
        self.enrollment_dao = EnrollmentDAO()

    def open_html(self, path):
        webbrowser.open(path)

    def generate_home_page(self):
        body_html = """
        <div class="dashboard-grid">
            <div class="card">
                <h3>Faculty Directory</h3>
                <p>View and review all professors currently in the system.</p>
                <a href="professors.html">Open Faculty Directory</a>
            </div>

            <div class="card">
                <h3>Student Directory</h3>
                <p>Review all students and their academic information.</p>
                <a href="students.html">Open Student Directory</a>
            </div>

            <div class="card">
                <h3>Course Catalog</h3>
                <p>View all courses and assigned faculty members.</p>
                <a href="courses.html">Open Course Catalog</a>
            </div>

            <div class="card">
                <h3>Student Reports</h3>
                <p>Generate student enrollment reports for advising and planning.</p>
                <a href="student_report_1.html">Open Sample Student Report</a>
            </div>

            <div class="card">
                <h3>Professor Reports</h3>
                <p>Generate faculty summary reports with assigned courses and enrollments.</p>
                <a href="professor_report_1.html">Open Sample Professor Report</a>
            </div>
        </div>
        """

        html_content = html_page(
            "Advisor Dashboard",
            "Academic Advisor Home",
            body_html
        )

        html_path = write_file("index.html", html_content)
        self.open_html(html_path)
        return f"Generated: {html_path}"

    def generate_all_professors_report(self):
        rows = self.professor_dao.get_all_professors()
        headers = ["Professor ID", "First Name", "Last Name", "Department", "Email"]

        html_content = html_page(
            "Faculty Directory",
            "Professor Directory",
            build_html_table(headers, rows)
        )
        md_content = build_markdown_table(headers, rows, "Faculty Directory")

        html_path = write_file("professors.html", html_content)
        md_path = write_file("professors.md", md_content)

        self.open_html(html_path)
        return f"Generated: {html_path} and {md_path}"

    def generate_all_students_report(self):
        rows = self.student_dao.get_all_students()
        headers = ["Student ID", "First Name", "Last Name", "Email", "Major", "Year"]

        html_content = html_page(
            "Student Directory",
            "Student Directory",
            build_html_table(headers, rows)
        )
        md_content = build_markdown_table(headers, rows, "Student Directory")

        html_path = write_file("students.html", html_content)
        md_path = write_file("students.md", md_content)

        self.open_html(html_path)
        return f"Generated: {html_path} and {md_path}"

    def generate_all_courses_report(self):
        rows = self.course_dao.get_all_courses()
        headers = [
            "Course ID",
            "Course Name",
            "Course Code",
            "Professor First Name",
            "Professor Last Name"
        ]

        html_content = html_page(
            "Course Catalog",
            "Course Catalog",
            build_html_table(headers, rows)
        )
        md_content = build_markdown_table(headers, rows, "Course Catalog")

        html_path = write_file("courses.html", html_content)
        md_path = write_file("courses.md", md_content)

        self.open_html(html_path)
        return f"Generated: {html_path} and {md_path}"

    def generate_student_enrollment_report(self, student_id):
        student_rows = self.student_dao.get_all_students()
        selected_student = None

        for student in student_rows:
            if str(student[0]) == str(student_id):
                selected_student = student
                break

        course_rows = self.enrollment_dao.get_courses_for_student(student_id)

        title = f"Student Enrollment Report - Student {student_id}"
        subtitle = "Student Enrollment Summary"

        if selected_student:
            subtitle = f"{selected_student[1]} {selected_student[2]} - Enrolled Courses"

        headers = ["Course ID", "Course Name", "Course Code"]

        html_content = html_page(
            title,
            subtitle,
            build_html_table(headers, course_rows)
        )
        md_content = build_markdown_table(headers, course_rows, title)

        html_path = write_file(f"student_report_{student_id}.html", html_content)
        md_path = write_file(f"student_report_{student_id}.md", md_content)

        self.open_html(html_path)
        return f"Generated: {html_path} and {md_path}"

    def generate_professor_summary_report(self, professor_id):
        conn = get_connection()
        cursor = conn.cursor()

        professor_query = """
        SELECT id, first_name, last_name, department, email
        FROM professor
        WHERE id = %s
        """
        cursor.execute(professor_query, (professor_id,))
        professor = cursor.fetchone()

        if not professor:
            cursor.close()
            conn.close()

            html_content = html_page(
                f"Professor Summary Report - Professor {professor_id}",
                "Professor Summary",
                '<div class="empty">Professor not found.</div>'
            )
            md_content = f"# Professor Summary Report - Professor {professor_id}\n\nProfessor not found."

            html_path = write_file(f"professor_report_{professor_id}.html", html_content)
            md_path = write_file(f"professor_report_{professor_id}.md", md_content)

            self.open_html(html_path)
            return f"Generated: {html_path} and {md_path}"

        course_query = """
        SELECT id, course_name, course_code
        FROM course
        WHERE professor_id = %s
        """
        cursor.execute(course_query, (professor_id,))
        courses = cursor.fetchall()

        sections_html = ""
        md_sections = []

        subtitle = f"{professor[1]} {professor[2]} - Professor Summary"

        if not courses:
            sections_html = '<div class="empty">This professor is not currently assigned to any courses.</div>'
            md_sections.append("This professor is not currently assigned to any courses.")
        else:
            for course in courses:
                enrollment_query = """
                SELECT student.id, student.first_name, student.last_name, student.email
                FROM enrollment
                JOIN student ON enrollment.student_id = student.id
                WHERE enrollment.course_id = %s
                """
                cursor.execute(enrollment_query, (course[0],))
                students = cursor.fetchall()

                course_title = f"{course[1]} ({course[2]})"

                sections_html += f"<h3>{course_title}</h3>"
                sections_html += build_html_table(
                    ["Student ID", "First Name", "Last Name", "Email"],
                    students
                )

                md_sections.append(f"## {course_title}")
                md_sections.append("")
                md_sections.append("| Student ID | First Name | Last Name | Email |")
                md_sections.append("| --- | --- | --- | --- |")

                if students:
                    for student in students:
                        md_sections.append(
                            f"| {student[0]} | {student[1]} | {student[2]} | {student[3]} |"
                        )
                else:
                    md_sections.append("| No enrolled students |  |  |  |")

                md_sections.append("")

        cursor.close()
        conn.close()

        html_content = html_page(
            f"Professor Summary Report - Professor {professor_id}",
            subtitle,
            sections_html
        )

        md_content = (
            f"# Professor Summary Report - Professor {professor_id}\n\n"
            + "\n".join(md_sections)
        )

        html_path = write_file(f"professor_report_{professor_id}.html", html_content)
        md_path = write_file(f"professor_report_{professor_id}.md", md_content)

        self.open_html(html_path)
        return f"Generated: {html_path} and {md_path}"