# P0-Akanksha-Satya

# Revature Institute of Technology  
### Academic Advisor Portal

#### http://127.0.0.1:5000/

This project is a full-stack academic management system built using Python, MySQL, and Flask. It allows users (academic advisors) to manage professors, students, courses, and enrollments through both a CLI and a web-based interface.

---

##  Features

###  Professor Management
- Add, view, update, and delete professors
- Assign professors to courses
- View courses taught by a professor

###  Student Management
- Add, view, update, and delete students
- Enroll students in courses
- Drop students from courses
- View courses for a student

###  Course Management
- Create and manage courses
- Assign or remove professors
- View enrolled students

###  Enrollment System
- Many-to-many relationship between students and courses
- Prevents duplicate enrollments

###  Reports
- View all professors, students, and courses
- Generate student enrollment reports
- Generate professor summary reports
- Reports available in HTML format

###  Web Interface (Flask)
- Academic advisor dashboard
- Search functionality
- Editable profiles
- Clean UI styled in Georgia Tech-inspired theme

---

##  Tech Stack

- **Backend:** Python
- **Web Framework:** Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS (Jinja templates)
- **Tools:** DBeaver, GitHub

---

##  Database Schema (ERD)

```mermaid
erDiagram
    PROFESSOR ||--o{ COURSE : teaches
    STUDENT ||--o{ ENROLLMENT : has
    COURSE ||--o{ ENROLLMENT : includes

    PROFESSOR {
        INT id PK
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR department
        VARCHAR email
    }

    STUDENT {
        INT id PK
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR email
        VARCHAR major
        VARCHAR year
    }

    COURSE {
        INT id PK
        VARCHAR course_name
        VARCHAR course_code
        INT professor_id FK
    }

    ENROLLMENT {
        INT id PK
        INT student_id FK
        INT course_id FK
        UNIQUE student_id_course_id
    }

