import PyPDF2
from jinja2 import FileSystemLoader, Environment


def parse_pdf(pdf_file):
    if pdf_file is isinstance(pdf_file, str):
        with open(pdf_file, "rb") as file:
            return _parse(file)
    else:
        return _parse(pdf_file)


def _parse(file):
    reader = PyPDF2.PdfReader(file)
    pdf_text = []
    num_pages = len(reader.pages)
    # Iterate over each page
    for page_number in range(num_pages):
        # Get the current page
        page = reader.pages[page_number]

        # Extract the text from the page
        page_text = page.extract_text()

        pdf_text.append(page_text)
    pdf_text = '\n'.join(pdf_text)
    return pdf_text, num_pages


def build_html_resume(data):
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('resume.html')
    html_resume = template.render(data)
    return html_resume


def export_html(html_resume, output_path):
    with open(output_path, 'w', encoding='utf8') as f:
        f.write(html_resume)
