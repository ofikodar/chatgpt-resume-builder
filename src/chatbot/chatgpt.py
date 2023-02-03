import ast
import json
import re
from pathlib import Path
from typing import Dict

from revChatGPT.ChatGPT import Chatbot

from .prompts import get_prompt


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

    @staticmethod
    def parse_json_from_string(input_string):
        try:
            start = input_string.index("{")
            end = input_string.rindex("}") + 1
            json_string = input_string[start:end]
        except ValueError:
            json_string = input_string
        return ast.literal_eval(json_string)

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