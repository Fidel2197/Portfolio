"""Build the public, one-page resume. Requires reportlab (pip install reportlab).

Run: python scripts/build_resume.py
Employment and education use the facts shared by the September 2026 resumes.
Public contact only; intentionally excludes a home address, phone, and
unconfirmed awards or clearance. Project descriptions reflect repository scope.
"""

from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "fidel-anyanwu-resume.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
PAGE_W, PAGE_H = 612, 792
LEFT, RIGHT = 40, 572
WIDTH = RIGHT - LEFT
INK = HexColor("#18343C")
MUTED = HexColor("#43555D")
TEAL = HexColor("#136B70")
RULE = HexColor("#C3D9D9")

c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H), invariant=1)
c.setTitle("Fidel Anyanwu | Software Development Resume")
c.setAuthor("Fidel Anyanwu")
c.setSubject("Public resume: projects, experience, education, and technical skills")
y = 752
body = ParagraphStyle("Body", fontName="Helvetica", fontSize=10.2, leading=13.6,
                      textColor=INK, alignment=TA_LEFT)


def para(text, gap=4, indent=0, size=None):
    global y
    style = body if size is None else ParagraphStyle(
        "Custom", parent=body, fontSize=size, leading=size + 2.8)
    p = Paragraph(text, style)
    _, h = p.wrap(WIDTH - indent, PAGE_H)
    y -= h
    p.drawOn(c, LEFT + indent, y)
    y -= gap


def section(title):
    global y
    y -= 16
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(LEFT, y, title.upper())
    c.setStrokeColor(RULE)
    c.setLineWidth(.6)
    c.line(LEFT, y - 5, RIGHT, y - 5)
    y -= 19


def role(title, organization, dates):
    global y
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 10.4)
    c.drawString(LEFT, y - 10, title)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9.5)
    c.drawRightString(RIGHT, y - 10, dates)
    y -= 14
    para(organization, gap=3, size=9.6)


def project(name, tech, description, url):
    para(f'<b><a href="{url}" color="#136B70">{name}</a></b>'
         f' <font color="#43555D">| {tech}</font>', gap=2)
    para(description, gap=6)


# Text-first, single-column layout preserves a straightforward reading order.
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 25)
c.drawString(LEFT, y, "FIDEL ANYANWU")
y -= 19
c.setFillColor(TEAL)
c.setFont("Helvetica", 10.4)
c.drawString(LEFT, y, "COMPUTER SCIENCE  /  SOFTWARE DEVELOPMENT")
y -= 17
para('<a href="mailto:fanyanwu@mcneese.edu">fanyanwu@mcneese.edu</a>'
     '  |  <a href="https://fidel-portfolio-eta.vercel.app/">Portfolio</a>'
     '  |  <a href="https://github.com/Fidel2197">GitHub: Fidel2197</a>'
     '  |  <a href="https://www.linkedin.com/in/fidel-anyanwu-98a34124b/">LinkedIn</a>', gap=8, size=9.3)
para('Computer Science senior with web application projects spanning data analysis, '
     'AI integration, and operational interfaces. Experience teaching programming labs, '
     'testing robotics prototypes, and supporting university residents.', gap=1)

section("Education")
para('<b>McNeese State University</b> | B.S. in Computer Science', gap=2)
para('Expected December 2026 | GPA: 3.50/4.00', gap=0)

section("Technical skills")
para('<b>Languages:</b> JavaScript, TypeScript, Python, SQL/T-SQL, HTML, CSS', gap=2)
para('<b>Applications &amp; data:</b> React, Next.js, FastAPI, pandas, NumPy, PostgreSQL, '
     'Supabase, SQL Server, REST APIs', gap=2)
para('<b>Tools &amp; practices:</b> Git/GitHub, Docker, Vercel, automated testing, debugging, '
     'technical documentation', gap=0)

section("Selected projects")
project('DataDock', 'React, FastAPI, pandas, PostgreSQL',
        'CSV analysis workspace with data-quality reports, charts, cleaning, and export. '
        'Includes accounts with private report history, account-isolation tests, and CI checks.',
        'https://github.com/Fidel2197/DataDock')
project('SnapChef', 'Next.js, TypeScript, Supabase, AI APIs',
        'Food-photo assistant with server-side image analysis, recipe results, preferences, '
        'authentication, and saved scan history; supports Gemini or OpenAI configuration.',
        'https://fidel-portfolio-eta.vercel.app/snapchef.html')
project('SignalDesk', 'Next.js, React, TypeScript, server routes',
        'Incident-response practice workspace with simulated incidents, triage, and response views. '
        'Separate integrations retrieve real public status signals from service providers.',
        'https://fidel-portfolio-eta.vercel.app/signaldesk.html')
project('CowboysBookstore', 'Team course project | Django REST, React, Docker',
        'Contributed workflow diagrams and documented testable requirements for registration, '
        'search, checkout, sessions, and administration in a collaborative bookstore project.',
        'https://fidel-portfolio-eta.vercel.app/bookstore.html')

section("Experience")
role('Resident Assistant', 'McNeese State University Housing', 'Aug 2024 - Present')
para('Support 50+ residents with housing questions, maintenance concerns, and campus resources. '
     'Mediate conflicts, document outcomes, and coordinate room checks, duty coverage, and programs.', gap=7)
role('Teaching Assistant', 'Department of Computing, McNeese State University', 'Aug 2023 - May 2024')
para('Led weekly JavaScript/HTML labs for 30+ students and reviewed 100+ assignments. '
     'Guided debugging and a browser Tetris project covering input, game loops, collision detection, '
     'scoring, and rendering.', gap=7)
role('Lab Research Assistant', 'McNeese Department of Computing and Engineering', 'Aug 2023 - May 2024')
para('Built and tested robotics prototypes; calibrated sensors, isolated hardware/control issues, '
     'and documented iterations. Presented prototype functionality and testing to 50+ '
     'Engineering Week attendees.', gap=0)

if y < 32:
    raise RuntimeError(f"Resume content exceeds one-page safe area (bottom={y:.1f}pt)")
c.showPage()
c.save()
print(f"Wrote {OUT} (content bottom: {y:.1f}pt)")
