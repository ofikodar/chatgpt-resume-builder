import streamlit as st

from src.chatbot.chatgpt import openai_key_info, Chatgpt
from src.chatbot.prompts import data_format
from src.data_handler import improve_resume, init_resume, download_pdf, update_resume_data, PDFSizeException
from src.exceptions import ChatbotInitException
from src.utils import is_new_file, is_data_loaded, key_to_tab_name, get_item_key, init_user_info

section_examples = {'summary': 'I have passion for new tech',
                    'workExperience': 'Tell about my ability to lead projects',
                    'education': 'Describe my degree type in more details',
                    'contactInfo': 'phone, Linkedin, etc.'}


def title():
    st.title("ChatCV - AI Resume Builder")


def resume_header():
    st.text_input('name', st.session_state.resume_data['name'], key="name")
    st.text_input('title', st.session_state.resume_data['title'], key="title")


def unknown_error():
    st.session_state['user_info'] = init_user_info(error_info, "It's just a glitch in the matrix."
                                                               " Try hitting refresh, and if that doesn't work, just imagine yourself in a peaceful place.")
    user_info()


def user_info():
    if not st.session_state.get('user_info'):
        upload_resume_header()

    message_type = st.session_state['user_info']['message_type']
    message = st.session_state['user_info']['message']
    message_type(message)


def upload_resume_header():
    st.session_state['user_info'] = init_user_info(st.success, "Upload PDF Resume - Let the magic begin. \n\n"
                                                               "This may take a bit... Grub a warm cup of coffee while we working :)")


def upload(uploaded_file):
    try:
        resume_data = init_resume(uploaded_file)
        st.session_state['user_info'] = init_user_info(success_info, "Working on it...")
        improve_resume(resume_data)

    except PDFSizeException:
        st.session_state['user_info'] = init_user_info(error_info, "PDF size max size is 4, try upload again...")

    except Exception:
        st.session_state['user_info'] = init_user_info(error_info, "PDF upload, try upload again...")


def sidebar():
    with st.sidebar:
        uploaded_file = st.file_uploader('Upload PDF Resume', type=["PDF"])
        if uploaded_file and is_new_file(uploaded_file):
            upload(uploaded_file)
            st.experimental_rerun()

        if is_data_loaded():
            st.button("Improve More", on_click=improve_resume)
            st.download_button('Download PDF', file_name='out.pdf', mime="application/json", data=download_pdf())


def body():
    section_dict = {'contactInfo': contact_info_section, 'summary': summary_section, 'workExperience': list_section,
                    'education': list_section, 'skills': skills_section}
    tabs_names = [key_to_tab_name(key) for key in section_dict.keys()]
    tabs = st.tabs(tabs_names)
    for tab, key in zip(tabs, section_dict):
        section_func = section_dict[key]
        with tab:
            section_func(key, st.session_state['resume_data'][key])


def init_chatbot():
    cols = st.columns([6, 1, 1])
    api_key = cols[0].text_input("Enter OpenAI API key")
    cols[1].markdown("#")
    api_submit = cols[1].button("Submit")

    cols[2].markdown("#")
    get_info = cols[2].button("Get key")
    if get_info:
        st.info(f"Get your key at: {openai_key_info}")
    if api_submit:
        if Chatgpt.validate_api(api_key):
            try:
                st.session_state['chatbot'] = Chatgpt(api_key)
            except ChatbotInitException:
                st.session_state['user_info'] = init_user_info(error_info,
                                                               "Error with Chatbot loadin, please refresh...")

            st.experimental_rerun()

        else:
            st.error("Not valid API key - try again...")


def summary_section(section_name, summary_data):
    st.text_area(section_name, summary_data, key=f'{section_name}', label_visibility='hidden')
    recruiter_subsection(section_name, section_examples[section_name])


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
        edit_list_subsection(section_name, section_data, item_id)

        st.markdown('***')


def edit_list_subsection(section_name, section_data, item_id):
    with st.container():
        st.markdown(
            """<style>
                .element-container:nth-of-type(1) button {
                    width: 100%;
                }
                </style>""",
            unsafe_allow_html=True,
        )

        remove_col, add_col = st.columns(2)
        if remove_col.button('Delete', key=f'{section_name}_{item_id}_remove_from_list') and len(section_data) > 1:
            del section_data[item_id]
            st.experimental_rerun()

        if add_col.button('Add', key=f'{section_name}_{item_id}_add_to_list') and len(section_data) < 10:
            section_data.append(data_format[section_name][0])
            st.experimental_rerun()


def recruiter_subsection(section_name, section_example, item_id=0):
    with st.container():
        cols = st.columns([3, 10], gap='small')
        cols[0].write('\n')
        cols[0].write('\n')
        button_clicked = cols[0].button("Auto Section Improve", key=f'{section_name}_{item_id}_improve_auto')
        trigger_key = 'Add a special request'
        user_request_template = f"{trigger_key} to the bot here... e.g. {section_example}."

        user_request = cols[1].text_input("section_example", value=user_request_template,
                                          key=f'{section_name}_{item_id}_improve_manual', label_visibility='hidden')
        if button_clicked:
            user_request = '' if trigger_key in user_request else user_request
            section_key = get_item_key(section_name, item_id)
            section_text = st.session_state[section_key]
            new_section_text = st.session_state['chatbot'].improve_section(section_text, user_request)

            update_resume_data(new_section_text, section_name, item_id)
            st.experimental_rerun()


def skills_section(section_name, skills_data):
    [skills_data.remove(skill) for skill in skills_data if not skill]

    num_columns = 3
    for skills_row in range(0, len(skills_data), num_columns):
        cols = st.columns([3, 1] * num_columns)
        skills_row_names = skills_data[skills_row: skills_row + num_columns]
        for item_id, skill in enumerate(skills_row_names):
            skill_id = skills_row + item_id
            cols[item_id * 2].text_input(' ', value=skill, key=f'{section_name}_{skill_id}', label_visibility='hidden')
            cols[item_id * 2 + 1].markdown('## ')
            if cols[item_id * 2 + 1].button('x', key=f'{section_name}_{skill_id}_remove_from_list'):
                del skills_data[skill_id]
                st.experimental_rerun()

    skill_subsection(section_name)
    st.markdown('***')


def skill_subsection(section_name, item_id=0):
    key = f'{section_name}_{item_id}_add_skill'
    cols = st.columns([12, 1])
    new_skill = cols[0].text_input("Add skill", key=key)
    cols[1].markdown('##')
    clicked = cols[1].button("\+")
    if clicked and new_skill:
        st.session_state['resume_data'][section_name].append(new_skill)
        st.experimental_rerun()


def contact_info_section(section_name, info_data):
    keys = sorted(info_data.keys())
    for key in keys:
        value = info_data[key]
        cols = st.columns([12, 1])
        cols[0].text_input(key.title(), value, key=f'{section_name}_{key}')
        cols[1].markdown('##')
        clicked = cols[1].button('\-', key=f'{section_name}_{key}_remove')
        if clicked:
            del info_data[key]
            st.experimental_rerun()

    add_contact_subsection(section_name, info_data)
    st.markdown('***')


def add_contact_subsection(section_name, info_data):
    st.markdown('***')

    with st.container():
        cols = st.columns([12, 1])
        new_key = cols[0].text_input('Add new details', value=f"e.g, {section_examples[section_name]}")
        cols[1].markdown('##')
        clicked = cols[1].button('\+', key=f'{section_name}_add_details')

        if clicked and new_key:
            info_data[new_key] = ''
            st.experimental_rerun()
    # if remove_col.button('Delete', key=f'{section_name}_{item_id}_remove_from_list') and len(section_data) > 1:
    #     del section_data[item_id]
    #     st.experimental_rerun()
    #
    # if add_col.button('Add', key=f'{section_name}_{item_id}_add_to_list') and len(section_data) < 10:
    #     section_data.append(data_format[section_name][0])
    #     st.experimental_rerun()


def success_info(message):
    st.success(message)


def error_info(message):
    st.error(message)
