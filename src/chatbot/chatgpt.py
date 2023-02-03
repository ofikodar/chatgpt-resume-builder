import ast
import json
import re
from pathlib import Path
from typing import Dict

from revChatGPT.ChatGPT import Chatbot

from .prompts import get_prompt, data_format


class Chatgpt:
    def __init__(self, config_path):
        session_token = self.load_session_token(config_path)
        self.conversation_id = None
        self.chatbot = Chatbot(session_token, conversation_id=self.conversation_id, parent_id=None)

    @staticmethod
    def load_session_token(config_path) -> Dict:
        """
        Load session token from config.json

        Returns:
            Dict: session token
        """
        config_file = Path(config_path)
        if not config_file.is_file():
            raise FileNotFoundError(f"config.json not found at {config_file.resolve()}")

        with open(config_file, 'r') as j_file:
            session_token = json.load(j_file)
        return session_token

    def improve_resume(self, parsed_resume: str) -> Dict:
        """
        Improves the given parsed resume using ChatGPT

        Args:
            parsed_resume (str): parsed resume data in string format

        Returns:
            Dict: improved resume data
        """
        chatgpt_input = get_prompt(parsed_resume, user_request='', output_type='all')
        response = self._ask(chatgpt_input)
        new_resume_data = self.parse_json_from_string(response)
        return new_resume_data

    def improve_section(self, section_text, user_request=''):
        chatgpt_input = get_prompt(section_text, user_request=user_request, output_type='section')
        response = self._ask(chatgpt_input)
        new_section_text = self.clean_section_response(response)
        return new_section_text

    def _ask(self, chatgpt_input):
        response = self.chatbot.ask(chatgpt_input, conversation_id=self.conversation_id, parent_id=None)
        self.conversation_id = response['conversation_id']
        return response['message']

    def clean_section_response(self, input_string):
        try:
            start = input_string.index('"')
            end = input_string.rindex('"') + 1
            input_string = input_string[start:end]
        except ValueError:
            pass
        input_string = self.remove_prefix(input_string)
        return input_string

    @staticmethod
    def remove_prefix(input_string):
        return re.sub(r'\w+:\n', '', input_string)

    def parse_json_from_string(self, json_string):
        clean_dict = dict()
        for key, value in data_format.items():
            pattern = ''
            if isinstance(value, str):
                pattern = f"'{key}':\s*'(\w*)'"
            elif isinstance(value, list):
                pattern = f"'{key}':\s*(\[.*\])"
            elif isinstance(value, dict):
                pattern = f"'{key}':" + "\s*(\{.*\})"

            extracted_value = self.extract_value(pattern, json_string)
            if extracted_value:
                try:
                    extracted_value = ast.literal_eval(extracted_value)
                except Exception:
                    pass

            if not isinstance(extracted_value, type(value)):
                extracted_value = ''
            clean_dict[key] = extracted_value

        return clean_dict

    def extract_value(self, pattern, string):
        match = re.search(pattern, string)

        if match:
            return match.group(1)
        else:
            return ''
