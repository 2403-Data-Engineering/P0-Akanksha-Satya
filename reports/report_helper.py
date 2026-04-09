import os
from datetime import datetime


OUTPUT_FOLDER = "reports/generated"


def ensure_output_folder():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def get_timestamp():
    return datetime.now().strftime("%B %d, %Y at %I:%M %p")


def html_page(title, subtitle, body_html):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            background-color: #f5f7fa;
            color: #1f2937;
        }}

        .header {{
            background: linear-gradient(135deg, #003057, #002147);
            color: white;
            padding: 24px 50px 18px 50px;
        }}

        .header h1 {{
            margin: 0;
            font-size: 32px;
        }}

        .header p {{
            margin: 8px 0 0;
            font-size: 15px;
            color: #e5e7eb;
        }}

        .nav {{
            margin-top: 18px;
        }}

        .nav a {{
            color: white;
            text-decoration: none;
            margin-right: 22px;
            font-weight: 500;
            font-size: 15px;
        }}

        .nav a:hover {{
            text-decoration: underline;
        }}

        .container {{
            max-width: 1100px;
            margin: 30px auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.08);
            padding: 30px;
        }}

        .section-title {{
            font-size: 22px;
            margin-bottom: 10px;
            color: #002147;
        }}

        .meta {{
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 20px;
        }}

        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 18px;
            margin-top: 20px;
        }}

        .card {{
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 20px;
        }}

        .card h3 {{
            margin-top: 0;
            color: #002147;
        }}

        .card p {{
            color: #4b5563;
            font-size: 14px;
        }}

        .card a {{
            display: inline-block;
            margin-top: 10px;
            color: #003057;
            font-weight: 600;
            text-decoration: none;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th {{
            background-color: #b3a369;
            color: #002147;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #e5e7eb;
        }}

        tr:nth-child(even) {{
            background-color: #f9fafb;
        }}

        .empty {{
            padding: 15px;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            background: #fafafa;
            color: #6b7280;
        }}

        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 12px;
            color: #9ca3af;
        }}

        h3 {{
            color: #002147;
            margin-top: 28px;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Revature Institute of Technology</h1>
        <p>Academic Advisor Portal • {subtitle}</p>
        <div class="nav">
            <a href="index.html">Home</a>
            <a href="professors.html">Professors</a>
            <a href="students.html">Students</a>
            <a href="courses.html">Courses</a>
        </div>
    </div>

    <div class="container">
        <div class="section-title">{title}</div>
        <div class="meta">Generated on {get_timestamp()}</div>
        {body_html}
        <div class="footer">
            Revature Institute of Technology • Internal Academic System
        </div>
    </div>
</body>
</html>
"""


def build_html_table(headers, rows):
    if not rows:
        return '<div class="empty">No records found.</div>'

    header_html = "".join(f"<th>{header}</th>" for header in headers)

    body_html = ""
    for row in rows:
        body_html += "<tr>"
        for value in row:
            body_html += f"<td>{value}</td>"
        body_html += "</tr>"

    return f"""
    <table>
        <thead>
            <tr>{header_html}</tr>
        </thead>
        <tbody>
            {body_html}
        </tbody>
    </table>
    """


def build_markdown_table(headers, rows, title):
    lines = [f"# {title}", ""]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    if rows:
        for row in rows:
            lines.append("| " + " | ".join(str(value) for value in row) + " |")
    else:
        empty_row = ["No records found."] + [""] * (len(headers) - 1)
        lines.append("| " + " | ".join(empty_row) + " |")

    return "\n".join(lines)


def write_file(filename, content):
    ensure_output_folder()
    path = os.path.join(OUTPUT_FOLDER, filename)

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

    return path