from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def update_resume_with_skills(skeleton, skills):
    """
    Replace the skills section in the resume skeleton with the updated skills.
    """
    skeleton["skills"] = skills
    return skeleton


# Step 4: Generate Resume in Specific Format
def add_hyperlink(paragraph, text, url):
    """
    Add a hyperlink to a paragraph.
    """
    # This gets access to the document XML
    part = paragraph.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)

    # Create the hyperlink element
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    # Create the run element for the text
    run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    r_style = OxmlElement('w:rStyle')
    r_style.set(qn('w:val'), "Hyperlink")
    rPr.append(r_style)
    run.append(rPr)

    # Add the text
    t = OxmlElement('w:t')
    t.text = text
    run.append(t)
    hyperlink.append(run)

    # Append the hyperlink to the paragraph
    paragraph._p.append(hyperlink)
    
def set_paragraph_spacing(paragraph, before=0, after=0, line_spacing=1):
    """
    Adjust the spacing of a paragraph.
    """
    paragraph_format = paragraph.paragraph_format
    paragraph_format.space_before = Pt(before)
    paragraph_format.space_after = Pt(after)
    paragraph_format.line_spacing = line_spacing

def add_horizontal_line(paragraph):
    """
    Add a horizontal line (border) to a paragraph.
    """
    p = paragraph._p  # Access the underlying XML paragraph element
    p_pr = p.get_or_add_pPr()
    p_borders = OxmlElement('w:pBdr')
    bottom_border = OxmlElement('w:bottom')
    bottom_border.set(qn('w:val'), 'single')
    bottom_border.set(qn('w:sz'), '4')  # Border size
    bottom_border.set(qn('w:space'), '1')
    bottom_border.set(qn('w:color'), 'auto')  # Black border
    p_borders.append(bottom_border)
    p_pr.append(p_borders)
