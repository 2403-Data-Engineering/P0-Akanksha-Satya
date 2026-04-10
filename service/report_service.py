import webbrowser


class ReportService:
    def open_student_report(self, student_id):
        path = f"reports/generated/student_report_{student_id}.html"
        webbrowser.open(path)
        return f"Opened {path}"

    def open_professor_report(self, professor_id):
        path = f"reports/generated/professor_report_{professor_id}.html"
        webbrowser.open(path)
        return f"Opened {path}"
