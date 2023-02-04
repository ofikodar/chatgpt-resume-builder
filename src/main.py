import ast
import re

from src.chatbot.prompts import data_format





if __name__ == '__main__':
    json_string = """
    {'name': 'cs', 'title': '2', 'contactInfo': {'linkedin': '', 'github': '', 'email': '', 'address': '', 'phone': ''},
     'summary': '','skills':['22','23','232'],
      'workExperience': [{'title': '878', 'company': '', 'dates': '', 'description': ''}, {'title': '', 'company': '', 'dates': '777', 'description': ''}],
        'education': [{'d}]
    """

    html_resume = x(json_string)
