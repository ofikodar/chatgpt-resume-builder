import ast
import json

import PyPDF2
import pdfkit
from jinja2 import FileSystemLoader, Environment
from reportlab.platypus import SimpleDocTemplate
from revChatGPT.ChatGPT import Chatbot

OUTPUT_FILE = 'output.html'
EXAMPLE_RESUME = r'C:\Users\ofiko\Downloads\ResumeParser-master\ResumeParser-master\data\input\example_resumes\Brendan_Herger_Resume.pdf'

DATA_FORMAT = {
    'name': '',
    'title': '',
    'linkedin': '',
    'github': '',
    'email': '',
    'summary': '',
    'work_experience': [
        {'title': '', 'company': '', 'dates': '', 'description': ''},
        {'title': '', 'company': '', 'dates': '', 'description': ''},
    ],
    'education': [
        {'degree': '', 'school': '', 'dates': '', 'description': ''},
    ],
    'skills': ['', '', '']
}
RESUME_PLACEHOLDER = '[$$$]'
START_RECRUITER_PROMPT = 'You are a recruiter. Here a parsed resume, re-write it as professional as possible, add valuable and missing critical information.'
DATA_FORMAT_PROMPT = F'Return a dictionary with the new data in this format: {str(DATA_FORMAT)}'
RESUME_PROMPT = f'This is the Resume: {RESUME_PLACEHOLDER}\n'
END_RECRUITER_PROMPT = '# professional it, add valuable and missing critical information, update it to maximize engament.'
PROMPT = '\n'.join([START_RECRUITER_PROMPT, DATA_FORMAT_PROMPT, RESUME_PROMPT, END_RECRUITER_PROMPT])


class Chatgpt:
    def __init__(self):
        session_token = self.load_session_token()
        self.chatbot = Chatbot(session_token, conversation_id=None,
                               parent_id=None)  # You can start a custom conversation

    @staticmethod
    def load_session_token():
        with open('config.json', 'r') as j_file:
            session_token = json.load(j_file)
        return session_token

    def ask(self, prompt):
        response = self.chatbot.ask(prompt, conversation_id=None,
                                    parent_id=None)
        return response


def parse_pdf(pdf_file):
    with open(pdf_file, "rb") as file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(file)
        pdf_text = []
        # Iterate over each page
        for page_number in range(len(reader.pages)):
            # Get the current page
            page = reader.pages[page_number]

            # Extract the text from the page
            page_text = page.extract_text()

            pdf_text.append(page_text)
    pdf_text = '\n'.join(pdf_text)
    return pdf_text

def _build_resume():


    with open('data.json', 'r') as f:
       data=  json.load( f)
    create_resume_html(data)

def _main():
    chatbot = Chatgpt()
    parsed_resume = parse_pdf(EXAMPLE_RESUME)
    chatgpt_input = PROMPT.replace(RESUME_PLACEHOLDER, parsed_resume)
    response = chatbot.ask(chatgpt_input)['message']
    data = ast.literal_eval(response)
    create_resume_html(data)


def create_resume_html(data):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('resume.html')
    output = template.render(data)
    with open(OUTPUT_FILE, 'w', encoding='utf8') as f:
        f.write(output)
    with open('data.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    _build_resume()
    # _main()