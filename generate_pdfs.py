from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
from reportlab.lib import colors

def save_as_pdf(data, pdf_file="resume.pdf"):
    """
    Generate a PDF directly using ReportLab with proper text wrapping, pagination, and empty headers for subsequent pages.
    """
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    margin = 50
    y = height - margin
    first_page = True

    def draw_line():
        """Draw a horizontal line."""
        nonlocal y
        c.line(margin, y, width - margin, y)
        y -= 20

    def add_wrapped_text_with_styles(prefix=None, text="", font="Helvetica", size=10, bold_prefix=False, wrap_width=90, indent=0):
        """
        Add wrapped text with optional bold prefixes and accurate wrapping logic.
        """
        nonlocal y, first_page

        # Ensure enough space for a new page
        if y < margin + size + 10:
            c.showPage()
            y = height - margin
            first_page = False
            draw_empty_header()

        c.setFont(font, size)

        # Combine prefix and text, if applicable
        full_text = f"{prefix}: {text}" if prefix else text

        # Accurate wrapping
        words = full_text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if c.stringWidth(test_line, font, size) <= (width - 2 * margin - indent):
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Draw each line
        for line in lines:
            x = margin + indent
            if prefix and bold_prefix and line.startswith(f"{prefix}:"):
                # Draw prefix in bold
                c.setFont("Helvetica-Bold", size)
                prefix_width = c.stringWidth(f"{prefix}: ", "Helvetica-Bold", size)
                c.drawString(x, y, f"{prefix}: ")
                c.setFont(font, size)
                c.drawString(x + prefix_width, y, line[len(f"{prefix}: "):])
            else:
                c.drawString(x, y, line)
            y -= size + 2

    def draw_empty_header():
        """Draw an empty header on pages after the first."""
        nonlocal y
        if not first_page:
            y = height - margin

    def add_contact_info():
        """
        Add contact information in one line with clickable hyperlinks.
        """
        nonlocal y
        contact_text = f"P: {data['header']['contact']['phone']} | LinkedIn | Email"
        text_width = c.stringWidth(contact_text, "Helvetica", 10)
        x = (width - text_width) / 2
        c.setFont("Helvetica", 10)

        # Add Phone
        c.drawString(x, y, f"P: {data['header']['contact']['phone']}")
        x += c.stringWidth(f"P: {data['header']['contact']['phone']} | ", "Helvetica", 10)

        # Add LinkedIn
        c.setFillColor(colors.blue)
        c.drawString(x, y, "LinkedIn")
        c.linkURL(data['header']['contact']['linkedin'], (x, y - 2, x + c.stringWidth("LinkedIn", "Helvetica", 10), y + 10), relative=0)
        x += c.stringWidth("LinkedIn | ", "Helvetica", 10)

        # Add Email
        c.drawString(x, y, "Email")
        c.linkURL(f"mailto:{data['header']['contact']['email']}", (x, y - 2, x + c.stringWidth("Email", "Helvetica", 10), y + 10), relative=0)
        c.setFillColor(colors.black)
        y -= 15

    # First Page Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString((width - c.stringWidth(data["header"]["name"], "Helvetica-Bold", 16)) / 2, y, data["header"]["name"])
    y -= 30

    # Add contact info
    add_contact_info()
    draw_line()

    # Summary Section
    add_wrapped_text_with_styles("Summary", data["summary"], font="Helvetica", size=12, bold_prefix=True)
    draw_line()

    # Education Section
    add_wrapped_text_with_styles("Education", font="Helvetica", size=12, bold_prefix=True)
    for edu in data["education"]:
        add_wrapped_text_with_styles(f"{edu['degree']} - {edu['university']}", bold_prefix=True)
        add_wrapped_text_with_styles(f"GPA: {edu.get('gpa', 'N/A')} ({edu.get('graduation_date', 'N/A')})")
    draw_line()

    # Technical Skills Section
    add_wrapped_text_with_styles("Technical Skills", font="Helvetica", size=12, bold_prefix=True)
    skills_data = data["skills"].get("Skills", {})
    for category, skills in skills_data.items():
        add_wrapped_text_with_styles(category, ", ".join(skills), bold_prefix=True)
    draw_line()

    # Work Experience Section
    add_wrapped_text_with_styles("Work Experience", font="Helvetica", size=12, bold_prefix=True)
    for exp in data["experience"]:
        add_wrapped_text_with_styles(f"{exp['title']} - {exp['company']} ({exp['duration']})", bold_prefix=True)
        for responsibility in exp.get("responsibilities", []):
            add_wrapped_text_with_styles(f"- {responsibility}", indent=10)
    draw_line()

    # Project Experience Section
    add_wrapped_text_with_styles("Project Experience", font="Helvetica", size=12, bold_prefix=True)
    for project in data["projects"]:
        add_wrapped_text_with_styles(project["name"], project["description"], bold_prefix=True)

    # Save the PDF
    c.save()
    print(f"PDF generated: {pdf_file}")
