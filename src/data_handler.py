import pdfkit
import streamlit as st

from src.exceptions import PDFSizeException
from src.pdf_handler import build_html_resume, parse_pdf
from src.utils import count_entries


def init_resume(uploaded_file):
    resume_data, num_pages = parse_pdf(uploaded_file)
    if num_pages > 3:
        raise PDFSizeException
    st.session_state['file_id'] = uploaded_file.id
    return resume_data


def update_resume_data(text_input, section_name, item_id=0):
    if section_name in ['workExperience', 'education']:
        key = 'description'
        st.session_state['resume_data'][section_name][item_id][key] = text_input
    elif section_name == 'summary':
        section_key = f'{section_name}'
        st.session_state['resume_data'][section_key] = text_input


def download_pdf():
    if st.session_state.get('name'):
        resume_data = format_resume_data()
    else:
        resume_data = st.session_state['resume_data']
    html_resume = build_html_resume(resume_data)
    options = {'page-size': 'A4', 'margin-top': '0.75in', 'margin-right': '0.75in', 'margin-bottom': '0.75in',
               'margin-left': '0.75in', 'encoding': "UTF-8", 'no-outline': None}
    return pdfkit.from_string(html_resume, options=options, css='src/css/main.css')


def improve_resume(resume_data=None):
    if resume_data is not None:
        st.session_state['resume_data'] = st.session_state['chatbot'].improve_resume(resume_data)
    else:
        st.session_state['resume_data'] = st.session_state['chatbot'].improve_resume(st.session_state['resume_data'])


def format_resume_data():
    current_state = st.session_state
    resume_data = {}
    contact_info = {}
    work_experience = []
    education = []
    skills = []

    resume_data['name'] = current_state.get('name', '')
    resume_data['title'] = current_state.get('title', '')

    contact_info_keys = ['linkedin', 'github', 'email', 'address']
    for key in contact_info_keys:
        contact_info[key] = current_state.get(f'contactInfo_{key}', '')

    resume_data['contactInfo'] = contact_info

    resume_data['summary'] = current_state.get('summary', '')

    work_experience_keys = ['workExperience_{}_title', 'workExperience_{}_company', 'workExperience_{}_dates',
                            'workExperience_{}_description']
    education_keys = ['education_{}_degree', 'education_{}_school', 'education_{}_dates', 'education_{}_description']

    total_work_experience = count_entries(st.session_state, 'workExperience')
    total_education = count_entries(st.session_state, 'education')

    for i in range(total_work_experience):
        work_experience.append(
            {key.split('_')[2]: current_state.get(key.format(i), '') for key in work_experience_keys})

    for i in range(total_education):
        education.append({key.split('_')[2]: current_state.get(key.format(i), '') for key in education_keys})

    resume_data['workExperience'] = work_experience
    resume_data['education'] = education

    total_skills = count_entries(st.session_state, 'skills')

    for i in range(total_skills):
        skill_key = f'skills_{i}'

        skills.append(current_state.get(skill_key, ''))
    resume_data['skills'] = skills
    return resume_data
