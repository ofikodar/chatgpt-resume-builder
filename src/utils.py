import re

import streamlit as st


def is_chatbot_loaded():
    return st.session_state.get('chatbot')


def is_new_file(uploaded_file):
    return uploaded_file.id != st.session_state.get('file_id', '')


def is_data_loaded():
    return st.session_state.get('resume_data')


def key_to_tab_name(input_string):
    return re.sub(r'([A-Z])', r' \1', input_string).strip().title()


def count_entries(input_dict, entry_type):
    max_index = max([int(key.split("_")[1]) for key in input_dict.keys() if key.startswith(f"{entry_type}_")],
                    default=0)
    return max_index + 1


def get_item_key(section_name, item_id=0):
    section_key = ''
    if section_name in ['workExperience', 'education']:
        key = 'description'
        section_key = f'{section_name}_{item_id}_{key}'
    elif section_name == 'summary':
        section_key = f'{section_name}'
    return section_key


def init_user_info(message_type, message):
    return {
        'message_type': message_type,
        'message': message
    }
