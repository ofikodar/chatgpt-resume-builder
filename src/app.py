import json

import streamlit as st

# Sample resume data
resume_data = {'name': 'John Doe', 'title': 'Data Scientist',

               'contactInfo': {'linkedin': 'linkedin.com/in/johndoe', 'github': 'github.com/johndoe',
                               'email': 'johndoe@email.com', 'address': '123 Main St, Anytown USA',

                               },

               'summary': 'Highly motivated and experienced data scientist with a passion for solving complex problems and finding insights in data. Skilled in using data to drive business decisions and improve processes.',
               'workExperience': [{'title': 'Data Scientist', 'company': 'ABC Company', 'dates': 'Jan 2018 - present',
                                   'description': 'Conducted data analysis and created predictive models to improve company sales and customer satisfaction.'},
                                  {'title': 'Data Analyst', 'company': 'XYZ Company', 'dates': 'Jan 2015 - Dec 2017',
                                   'description': 'Collected and analyzed data to support decision-making and improve company operations.'}, ],
               'education': [{'degree': 'Master of Science in Data Science', 'school': 'University of Technology',
                              'dates': 'Jan 2013 - Dec 2014',
                              'description': 'Focus on machine learning and data visualization techniques.'},
                             {'degree': 'Bachelor of Science in Computer Science', 'school': 'University of Science',
                              'dates': 'Jan 2009 - Dec 2012',
                              'description': 'Focus on software development and algorithms.'}, ],
               'skills': ['Data analysis', 'Predictive modeling', 'Machine learning', 'Data visualization',
                          'Software development']}

section_examples = {'summary': 'I have passion for new tech',
                    'workExperience': 'Tell about my ability to lead projects',
                    'education': 'Describe my degree type in more detail', 'skills': 'Add soft skills'}


def list_section(section_name, section_data):
    description_key = 'description'

    item_keys = list(section_data[0].keys())
    item_keys.remove(description_key)
    for item_id, section_item in enumerate(section_data):
        cols = st.columns(len(item_keys))
        for col, key in zip(cols, item_keys):
            col.text_input(key, section_item[key], key=f'{section_name}_{item_id}_{key}')
        st.text_area(description_key, section_item[description_key], key=f'{section_name}_{item_id}_{description_key}')

        recruiter_subsection(section_name, section_example=section_examples[section_name], item_id=item_id)
        st.markdown('***')


def skills_section(section_name, skills_data):
    num_columns = 3
    for skills_row in range(0, len(skills_data), num_columns):
        cols = st.columns([3, 1] * num_columns)
        skills_row_names = skills_data[skills_row: skills_row + num_columns]
        for item_id, skill in enumerate(skills_row_names):
            skill_id = skills_row + item_id
            cols[item_id * 2].text_input('', value=skill, key=f'{section_name}_{skill_id}', label_visibility='hidden')
            cols[item_id * 2 + 1].markdown('# ')
            cols[item_id * 2 + 1].button('x', key=f'{section_name}_{skill_id}_remove_skill')

    skill_subsection(section_name)
    recruiter_subsection(section_name, section_example=section_examples[section_name])
    st.markdown('***')


def skill_subsection(section_name, item_id=0):
    st.text_input("Add skill", key=f'{section_name}_{item_id}_add_skill')


def recruiter_subsection(section_name, section_example, item_id=0):
    with st.container():
        cols = st.columns([3, 10], gap='small')
        cols[0].write('\n')
        cols[0].write('\n')
        cols[0].button("Auto Section Improve", key=f'{section_name}_{item_id}_improve_auto')
        cols[1].text_input("section_example",
                           value=f"Send a special request to the bot here... e.g. {section_example}.",
                           key=f'{section_name}_{item_id}_improve_manual', label_visibility='hidden')


def summary_section(section_name, summary_data):
    st.text_area(section_name, summary_data, key=f'{section_name}', label_visibility='hidden')
    recruiter_subsection(section_name, section_examples[section_name])


def contact_info_section(section_name, info_data):
    for key, value in info_data.items():
        if value:
            st.text_input(key.title(), value, key=f'{section_name}_{key}')
    st.markdown('***')


def title():
    st.text_input('name', st.session_state.resume_data['name'], key="name")
    st.text_input('title', st.session_state.resume_data['title'], key="title")


def body():
    section_dict = {'contactInfo': contact_info_section, 'summary': summary_section, 'workExperience': list_section,
                    'education': list_section, 'skills': skills_section}
    tabs_names = [key.replace('_', ' ').title() for key in section_dict.keys()]
    tabs = st.tabs(tabs_names)
    for tab, key in zip(tabs, section_dict):
        section_func = section_dict[key]
        with tab:
            section_func(key, st.session_state['resume_data'][key])


def sidebar():
    with st.sidebar:
        st.file_uploader('Upload PDF Resume', type="pdf")
        st.button("Auto Improve All")
        st.button("Give Feedback")
        st.download_button('Download PDF', file_name='output.json', mime="application/json",
                           data=json.dumps(format_resume_data()))


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


def count_entries(input_dict, entry_type):
    max_index = max([int(key.split("_")[1]) for key in input_dict.keys() if key.startswith(f"{entry_type}_")],
                    default=0)
    return max_index + 1


def header():
    st.title("SolidCV - AI Resume Improver")


def _main():
    if 'resume_data' not in st.session_state:
        st.session_state['resume_data'] = resume_data
    header()
    title()
    body()
    sidebar()


if __name__ == '__main__':
    _main()

    # bootstrap 4 collapse example
