import streamlit as st

# Sample resume data
DATA_FORMAT = {'name': 'John Doe', 'title': 'Data Scientist',

               'contact_info': {'linkedin': 'linkedin.com/in/johndoe', 'github': 'github.com/johndoe',
                                'email': 'johndoe@email.com', 'address': '123 Main St, Anytown USA',

                                },

               'summary': 'Highly motivated and experienced data scientist with a passion for solving complex problems and finding insights in data. Skilled in using data to drive business decisions and improve processes.',
               'work_experience': [{'title': 'Data Scientist', 'company': 'ABC Company', 'dates': 'Jan 2018 - present',
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


# Set the CSS style for the app
def set_style():
    with open('src/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Use the set_style function to add CSS to the app

# Add header and input fields to the app

def list_section(section_name, section_data):
    description_key = 'description'

    item_keys = list(section_data[0].keys())
    item_keys.remove(description_key)
    for section_id, section_item in enumerate(section_data):
        cols = st.columns(len(item_keys))
        for col, key in zip(cols, item_keys):
            col.text_input(key, section_item[key], key=f'{section_name}_{section_id}_{key}')
        st.text_area(description_key, section_item[description_key])

    with st.container():
        cols = st.columns(2)
        cols[0].button("Auto Improve", key=f'{section_name}_improve_auto')
        cols[1].text_input("Ask a recruiter", key=f'{section_name}_improve_manual')


def skills_section(section_name, skills_data):
    for skill in skills_data:
        st.info(skill)

    with st.container():
        cols = st.columns(2)
        cols[0].button("Auto Improve", key=f'{section_name}_improve_auto')
        cols[1].text_input("Free Text", key=f'{section_name}_improve_manual')


def summary_section(section_name, summary_data):
    st.text_area('', summary_data, key=f'{section_name}')
    with st.container():
        cols = st.columns(2)
        cols[0].button("Auto Improve", key=f'{section_name}_improve_auto')
        cols[1].text_input("Ask a recruiter", key=f'{section_name}_improve_manual')


def contact_info_section(section_name, info_data):
    for key, value in info_data.items():
        if value:
            st.text_input(key.title(), value)


def title(DATA_FORMAT):
    st.text_input('name', DATA_FORMAT['name'])
    st.text_input('title', DATA_FORMAT['title'])


def body(DATA_FORMAT):
    section_dict = {'contact_info': contact_info_section, 'summary': summary_section, 'work_experience': list_section,
                    'education': list_section, 'skills': skills_section}

    tabs_names = [key.replace('_', ' ').title() for key in section_dict.keys()]
    tabs = st.tabs(tabs_names)
    for tab, key in zip(tabs, section_dict):
        section_func = section_dict[key]
        with tab:
            section_func(key, DATA_FORMAT[key])


def sidebar():
    with st.sidebar:
        st.file_uploader('Upload PDF Resume', type="pdf")
        st.button("Auto Improve All")
        st.button("Give Feedback")
        st.download_button('Download PDF', 'text_contents')

def header():
    st.title("SolidCV - AI Resume Improver")

def _main(DATA_FORMAT):
    header()
    title(DATA_FORMAT)
    body(DATA_FORMAT)
    sidebar()


if __name__ == '__main__':
    _main(DATA_FORMAT)

    # bootstrap 4 collapse example
