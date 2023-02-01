from langchain import OpenAI, PromptTemplate

prompt_placeholder = '[$$$]'

data_format = {'name': '', 'title': '',
               'contactInfo': {'linkedin': '', 'github': '', 'email': '', 'address': '', 'phone': ''}, 'summary': '',
               'workExperience': [{'title': '', 'company': '', 'dates': '', 'description': ''},
                                  {'title': '', 'company': '', 'dates': '', 'description': ''}, ],
               'education': [{'degree': '', 'school': '', 'dates': '', 'description': ''}, ], 'skills': ['', '', '']}

recruiter_prompt = 'You are a recruiter and a professional resume builder.'
command_prompt = 'Re-write the input as professionally as possible, adding vital and valuable information.'
user_request_prompt = f'{prompt_placeholder}'
output_format_prompts = dict()
output_format_prompts['all'] = f'Return the output as dictionary in the next format {str(data_format)}.'
output_format_prompts['section'] = f'Return the output as string.'

input_prompt = f'Input: {prompt_placeholder}'


def get_prompt(command_type, input_data ,user_request=''):
    valid_command_types = list(output_format_prompts)
    assert command_type in valid_command_types, f"Not valid command type, try {valid_command_types}"
    if user_request:
        user_request += '\n'

    template = '\n'.join(
        [recruiter_prompt, command_prompt, user_request_prompt.replace(prompt_placeholder, user_request), input_prompt.replace(prompt_placeholder, input_data), output_format_prompts[command_type]])
    return template

command_type = 'all'
template = get_prompt(command_type,'xx','sfdsf')
print(template)
