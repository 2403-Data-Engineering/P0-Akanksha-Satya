from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from io import BytesIO
from fpdf import FPDF

from service.student_service import StudentService
from service.professor_service import ProfessorService
from service.course_service import CourseService
from service.enrollment_service import EnrollmentService

app = Flask(__name__)
app.secret_key = "revature_institute_secret"

student_service = StudentService()
professor_service = ProfessorService()
course_service = CourseService()
enrollment_service = EnrollmentService()


def is_valid_numeric_id(value):
    return str(value).isdigit()


def build_pdf(title, lines):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_x(15)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.set_font("Helvetica", size=11)

    usable_width = 180  # safe width for letter/A4 style pages with margins

    for line in lines:
        pdf.set_x(15)

        text = str(line).replace("\t", "    ").strip()
        if text == "":
            pdf.ln(6)
        else:
            pdf.multi_cell(usable_width, 8, text)

    pdf_bytes = bytes(pdf.output(dest="S"))
    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)
    return buffer


@app.route("/")
def home():
    return render_template("dashboard.html")


# ---------------- STUDENTS ----------------

@app.route("/students")
def students():
    query = request.args.get("q", "").strip()
    students = student_service.search_students(query) if query else student_service.get_all_students()
    return render_template("students.html", students=students, query=query)


@app.route("/students/add", methods=["POST"])
def add_student():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()
    major = request.form.get("major", "").strip()
    year = request.form.get("year", "").strip()

    if not first_name or not last_name or not email:
        flash("Please complete the required student fields.", "error")
        return redirect(url_for("students"))

    message = student_service.add_student(first_name, last_name, email, major, year)
    flash(message, "success")
    return redirect(url_for("students"))


@app.route("/students/<student_id>")
def student_detail(student_id):
    if not is_valid_numeric_id(student_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("students"))

    student = student_service.get_student_by_id(student_id)
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for("students"))

    enrolled_courses = enrollment_service.get_courses_for_student(student_id)
    all_courses = course_service.get_all_courses()
    return render_template(
        "student_detail.html",
        student=student,
        enrolled_courses=enrolled_courses,
        all_courses=all_courses
    )


@app.route("/students/<student_id>/delete", methods=["POST"])
def delete_student(student_id):
    if not is_valid_numeric_id(student_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("students"))

    message = student_service.remove_student(student_id)
    flash(message, "success" if "removed" in message.lower() else "error")
    return redirect(url_for("students"))


@app.route("/students/<student_id>/enroll", methods=["POST"])
def enroll_student_from_student_page(student_id):
    course_id = request.form.get("course_id", "").strip()

    if not is_valid_numeric_id(student_id) or not is_valid_numeric_id(course_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("student_detail", student_id=student_id))

    message = enrollment_service.enroll_student(student_id, course_id)
    flash(message, "success" if "successfully" in message.lower() else "error")
    return redirect(url_for("student_detail", student_id=student_id))
@app.route("/students/<student_id>/edit", methods=["POST"])
def edit_student(student_id):
    if not is_valid_numeric_id(student_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("students"))

    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()
    major = request.form.get("major", "").strip()
    year = request.form.get("year", "").strip()

    if not first_name or not last_name or not email:
        flash("Please complete the required student fields.", "error")
        return redirect(url_for("student_detail", student_id=student_id))

    message = student_service.update_student(student_id, first_name, last_name, email, major, year)
    flash(message, "success")
    return redirect(url_for("student_detail", student_id=student_id))


@app.route("/students/<student_id>/drop/<course_id>", methods=["POST"])
def drop_student_from_course(student_id, course_id):
    if not is_valid_numeric_id(student_id) or not is_valid_numeric_id(course_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("student_detail", student_id=student_id))

    message = enrollment_service.drop_student(student_id, course_id)
    flash(message, "success")
    return redirect(url_for("student_detail", student_id=student_id))
@app.route("/reports/student/<student_id>")
def student_report_view(student_id):
    if not is_valid_numeric_id(student_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("reports"))

    student = student_service.get_student_by_id(student_id)
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for("reports"))

    courses = enrollment_service.get_courses_for_student(student_id)
    return render_template("student_report.html", student=student, courses=courses)



# ---------------- PROFESSORS ----------------

@app.route("/professors")
def professors():
    query = request.args.get("q", "").strip()
    professors = professor_service.search_professors(query) if query else professor_service.get_all_professors()
    return render_template("professors.html", professors=professors, query=query)


@app.route("/professors/add", methods=["POST"])
def add_professor():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    department = request.form.get("department", "").strip()
    email = request.form.get("email", "").strip()

    if not first_name or not last_name or not email:
        flash("Please complete the required professor fields.", "error")
        return redirect(url_for("professors"))

    message = professor_service.add_professor(first_name, last_name, department, email)
    flash(message, "success")
    return redirect(url_for("professors"))


@app.route("/professors/<professor_id>")
def professor_detail(professor_id):
    if not is_valid_numeric_id(professor_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("professors"))

    professor = professor_service.get_professor_by_id(professor_id)
    if not professor:
        flash("Professor not found.", "error")
        return redirect(url_for("professors"))

    courses = course_service.get_courses_by_professor(professor_id)
    return render_template("professor_detail.html", professor=professor, courses=courses)


@app.route("/professors/<professor_id>/delete", methods=["POST"])
def delete_professor(professor_id):
    if not is_valid_numeric_id(professor_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("professors"))

    message = professor_service.remove_professor(professor_id)
    flash(message, "success" if "removed" in message.lower() else "error")
    return redirect(url_for("professors"))
@app.route("/professors/<professor_id>/unassign/<course_id>", methods=["POST"])
def unassign_professor_from_course(professor_id, course_id):
    if not is_valid_numeric_id(professor_id) or not is_valid_numeric_id(course_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("professor_detail", professor_id=professor_id))

    message = course_service.unassign_professor_from_course(course_id)
    flash(message, "success")
    return redirect(url_for("professor_detail", professor_id=professor_id))
@app.route("/professors/<professor_id>/edit", methods=["POST"])
def edit_professor(professor_id):
    if not is_valid_numeric_id(professor_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("professors"))

    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    department = request.form.get("department", "").strip()
    email = request.form.get("email", "").strip()

    if not first_name or not last_name or not email:
        flash("Please complete the required professor fields.", "error")
        return redirect(url_for("professor_detail", professor_id=professor_id))

    message = professor_service.update_professor(
        professor_id, first_name, last_name, department, email
    )
    flash(message, "success" if "updated" in message.lower() else "error")
    return redirect(url_for("professor_detail", professor_id=professor_id))
@app.route("/reports/professor/<professor_id>")
def professor_report_view(professor_id):
    if not is_valid_numeric_id(professor_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("reports"))

    professor = professor_service.get_professor_by_id(professor_id)
    if not professor:
        flash("Professor not found.", "error")
        return redirect(url_for("reports"))

    courses = course_service.get_courses_by_professor(professor_id)

    course_data = []
    for course in courses:
        students = enrollment_service.get_students_in_course(course[0])
        course_data.append({
            "course": course,
            "students": students
        })

    return render_template("professor_report.html", professor=professor, course_data=course_data)

# ---------------- COURSES ----------------

@app.route("/courses")
def courses():
    query = request.args.get("q", "").strip()
    courses = course_service.search_courses(query) if query else course_service.get_all_courses()
    professors = professor_service.get_all_professors()
    return render_template("courses.html", courses=courses, professors=professors, query=query)


@app.route("/courses/add", methods=["POST"])
def add_course():
    course_name = request.form.get("course_name", "").strip()
    course_code = request.form.get("course_code", "").strip()
    professor_id = request.form.get("professor_id", "").strip()

    if not course_name or not course_code or not professor_id:
        flash("Please complete the required course fields.", "error")
        return redirect(url_for("courses"))

    if not is_valid_numeric_id(professor_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("courses"))

    message = course_service.add_course(course_name, course_code, professor_id)
    flash(message, "success" if "added" in message.lower() else "error")
    return redirect(url_for("courses"))


@app.route("/courses/<course_id>")
def course_detail(course_id):
    if not is_valid_numeric_id(course_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("courses"))

    course = course_service.get_course_by_id(course_id)
    if not course:
        flash("Course not found.", "error")
        return redirect(url_for("courses"))

    students_in_course = enrollment_service.get_students_in_course(course_id)
    all_students = student_service.get_all_students()
    return render_template(
        "course_detail.html",
        course=course,
        students_in_course=students_in_course,
        all_students=all_students
    )


@app.route("/courses/<course_id>/delete", methods=["POST"])
def delete_course(course_id):
    if not is_valid_numeric_id(course_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("courses"))

    message = course_service.remove_course(course_id)
    flash(message, "success" if "removed" in message.lower() else "error")
    return redirect(url_for("courses"))


@app.route("/courses/<course_id>/enroll", methods=["POST"])
def enroll_student_from_course_page(course_id):
    student_id = request.form.get("student_id", "").strip()

    if not is_valid_numeric_id(course_id) or not is_valid_numeric_id(student_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("course_detail", course_id=course_id))

    message = enrollment_service.enroll_student(student_id, course_id)
    flash(message, "success" if "successfully" in message.lower() else "error")
    return redirect(url_for("course_detail", course_id=course_id))


# ---------------- REPORTS ----------------

@app.route("/reports")
def reports():
    students = student_service.get_all_students()
    professors = professor_service.get_all_professors()
    courses = course_service.get_all_courses()
    return render_template("reports.html", students=students, professors=professors, courses=courses)


@app.route("/reports/student/<student_id>/pdf")
def student_report_pdf(student_id):
    if student_id == "all":
        students = student_service.get_all_students()

        lines = ["All Students Report", ""]
        for student in students:
            lines.append(
                f"ID: {student[0]} | {student[1]} {student[2]} | {student[3]} | {student[4]} | Year: {student[5]}"
            )

        pdf_buffer = build_pdf("All Students Report", lines)
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="all_students_report.pdf",
            mimetype="application/pdf"
        )

    if not is_valid_numeric_id(student_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("reports"))

    student = student_service.get_student_by_id(student_id)
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for("reports"))

    courses = enrollment_service.get_courses_for_student(student_id)

    lines = [
        f"Student ID: {student[0]}",
        f"Name: {student[1]} {student[2]}",
        f"Email: {student[3]}",
        f"Major: {student[4]}",
        f"Year: {student[5]}",
        "",
        "Enrolled Courses:"
    ]

    if courses:
        for course in courses:
            lines.append(f"- {course[1]} ({course[2]})")
    else:
        lines.append("No courses found.")

    pdf_buffer = build_pdf("Student Enrollment Report", lines)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"student_report_{student_id}.pdf",
        mimetype="application/pdf"
    )


@app.route("/reports/professor/<professor_id>/pdf")
def professor_report_pdf(professor_id):
    if professor_id == "all":
        professors = professor_service.get_all_professors()

        lines = ["All Professors Report", ""]
        for professor in professors:
            lines.append(
                f"ID: {professor[0]} | {professor[1]} {professor[2]} | {professor[3]} | {professor[4]}"
            )

        pdf_buffer = build_pdf("All Professors Report", lines)
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="all_professors_report.pdf",
            mimetype="application/pdf"
        )

    if not is_valid_numeric_id(professor_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("reports"))

    professor = professor_service.get_professor_by_id(professor_id)
    if not professor:
        flash("Professor not found.", "error")
        return redirect(url_for("reports"))

    courses = course_service.get_courses_by_professor(professor_id)

    lines = [
        f"Professor ID: {professor[0]}",
        f"Name: {professor[1]} {professor[2]}",
        f"Department: {professor[3]}",
        f"Email: {professor[4]}",
        "",
        "Assigned Courses and Enrollments:"
    ]

    if courses:
        for course in courses:
            lines.append("")
            lines.append(f"{course[1]} ({course[2]})")
            students = enrollment_service.get_students_in_course(course[0])
            if students:
                for student in students:
                    lines.append(f"  - {student[1]} {student[2]} ({student[3]})")
            else:
                lines.append("  - No enrolled students")
    else:
        lines.append("No courses found.")

    pdf_buffer = build_pdf("Professor Summary Report", lines)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"professor_report_{professor_id}.pdf",
        mimetype="application/pdf"
    )

@app.route("/reports/course/<course_id>/pdf")
def course_report_pdf(course_id):
    if course_id == "all":
        courses = course_service.get_all_courses()

        lines = ["All Courses Report", ""]
        for course in courses:
            lines.append(
                f"Course ID: {course[0]} | Name: {course[1]} | Code: {course[2]} | Professor: {course[3]} {course[4]}"
            )

        pdf_buffer = build_pdf("All Courses Report", lines)
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="all_courses_report.pdf",
            mimetype="application/pdf"
        )

    if not is_valid_numeric_id(course_id):
        flash("Invalid ID. Please enter a number.", "error")
        return redirect(url_for("reports"))

    course = course_service.get_course_by_id(course_id)
    if not course:
        flash("Course not found.", "error")
        return redirect(url_for("reports"))

    students = enrollment_service.get_students_in_course(course_id)

    lines = [
        f"Course ID: {course[0]}",
        f"Course Name: {course[1]}",
        f"Course Code: {course[2]}",
        f"Professor ID: {course[3]}",
        f"Professor: {course[4]} {course[5]}",
        "",
        "Enrolled Students:"
    ]

    if students:
        for student in students:
            lines.append(f"- {student[1]} {student[2]} ({student[3]})")
    else:
        lines.append("No students enrolled.")

    pdf_buffer = build_pdf("Course Report", lines)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"course_report_{course_id}.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)