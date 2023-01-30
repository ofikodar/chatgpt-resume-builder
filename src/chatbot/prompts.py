DATA_FORMAT = {'name': '', 'title': '',
               'contact_info': {'linkedin': '', 'github': '', 'email': '', 'address': '', 'phone': ''}, 'summary': '',
               'work_experience': [{'title': '', 'company': '', 'dates': '', 'description': ''},
                                   {'title': '', 'company': '', 'dates': '', 'description': ''}, ],
               'education': [{'degree': '', 'school': '', 'dates': '', 'description': ''}, ], 'skills': ['', '', '']}

RESUME_PLACEHOLDER = '[$$$]'
START_RECRUITER_PROMPT = 'You are a recruiter. Here a parsed resume, re-write it as professional as possible, add valuable and missing critical information.'
DATA_FORMAT_PROMPT = F'Return a dictionary with the new data in this format: {str(DATA_FORMAT)}'
RESUME_PROMPT = f'This is the Resume: {RESUME_PLACEHOLDER}\n'
END_RECRUITER_PROMPT = '# professional it, add valuable and missing critical information, update it to maximize engament. Expand descriptions and skills.'
PROMPT = '\n'.join([START_RECRUITER_PROMPT, DATA_FORMAT_PROMPT, RESUME_PROMPT, END_RECRUITER_PROMPT])
