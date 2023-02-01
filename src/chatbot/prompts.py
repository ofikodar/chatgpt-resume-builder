from langchain import OpenAI, PromptTemplate

data_format = {'name': '', 'title': '',
               'contactInfo': {'linkedin': '', 'github': '', 'email': '', 'address': '', 'phone': ''}, 'summary': '',
               'workExperience': [{'title': '', 'company': '', 'dates': '', 'description': ''},
                                  {'title': '', 'company': '', 'dates': '', 'description': ''}, ],
               'education': [{'degree': '', 'school': '', 'dates': '', 'description': ''}, ], 'skills': ['', '', '']}

recruiter_prompt = 'You are a recruiter and a professional resume builder.'
command_prompt = 'Re-write the input as professionally as possible, adding vital and valuable information.'

output_format_prompts = dict()
output_format_prompts['all'] = f'Return the output as dictionary in the next format {str(data_format)}.'
output_format_prompts['section'] = f'Return the output as string.'

input_prompt = 'Input: {input}'


def get_template(command_type, spacial_request_prompt=''):
    valid_command_types = list(output_format_prompts)
    assert command_type in valid_command_types, f"Not valid command type, try {valid_command_types}"
    if spacial_request_prompt:
        spacial_request_prompt += '\n'
    template = '\n'.join([recruiter_prompt, command_prompt, spacial_request_prompt, input_prompt , output_format_prompts[command_type]])
    return template

print(get_template('all','ASD'))
