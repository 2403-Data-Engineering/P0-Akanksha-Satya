from reports.advisor_portal import AdvisorPortal


class ReportService:
    def __init__(self):
        self.portal = AdvisorPortal()

    def generate_home_page(self):
        return self.portal.generate_home_page()

    def generate_student_enrollment_report(self, student_id):
        return self.portal.generate_student_enrollment_report(student_id)

    def generate_professor_summary_report(self, professor_id):
        return self.portal.generate_professor_summary_report(professor_id)

    def generate_all_professors_report(self):
        return self.portal.generate_all_professors_report()

    def generate_all_students_report(self):
        return self.portal.generate_all_students_report()

    def generate_all_courses_report(self):
        return self.portal.generate_all_courses_report()