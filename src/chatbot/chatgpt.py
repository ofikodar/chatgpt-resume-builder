import ast
import json
import logging
import re
from pathlib import Path
from typing import Dict

import requests
from revChatGPT.Official import Chatbot

from src.chatbot.prompts import get_prompt, data_format

logging.basicConfig(filename='chatgpt.log', level=logging.INFO, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

openai_key_info = 'https://platform.openai.com/account/api-keys'


class Chatgpt:
    def __init__(self, api_key):
        self.chatbot = Chatbot(api_key)
        logging.info("API key loaded successfully")

    @staticmethod
    def validate_api(api_key):
        if api_key and api_key.startswith("sk-") and len(api_key) > 50:
            response = requests.get("https://api.openai.com/v1/engines", headers={"Authorization": f"Bearer {api_key}"})
            return response.status_code == 200
        return False

    @staticmethod
    def load_api_key(config_path):
        """
        Load api key from config.json

        Returns:
            Str: session token
        """
        config_file = Path(config_path)
        if not config_file.is_file():
            raise FileNotFoundError(f"config.json not found at {config_file.resolve()}")

        with open(config_file, 'r') as j_file:
            session_token = json.load(j_file)
        return session_token['api_key']

    def improve_resume(self, parsed_resume: str) -> Dict:
        logging.info("Improving parsed resume")
        chatgpt_input = get_prompt(parsed_resume, user_request='', output_type='all')
        response = self._ask(chatgpt_input)
        new_resume_data = self.parse_json_from_string(response)
        logging.info("Resume improved successfully")
        return new_resume_data

    def improve_section(self, section_text, user_request=''):
        logging.info("Improving section")
        chatgpt_input = get_prompt(section_text, user_request=user_request, output_type='section')
        response = self._ask(chatgpt_input)
        new_section_text = self.clean_section_response(response)
        logging.info("Section improved successfully")
        return new_section_text

    def _ask(self, chatgpt_input):
        logging.info("Asking chatbot for response")
        try:
            response = self.chatbot.ask(chatgpt_input)
            answer = response['choices'][0]['text']
            logging.info("Received response from chatbot")
            logging.info(f"Response: {answer}")
        except Exception:
            answer = ""
        return answer

    def parse_json_from_string(self, json_string):

        try:
            return ast.literal_eval(json_string)
        except Exception:
            logging.error("Error in parsing JSON string")

        json_string = re.sub('\s+', ' ', json_string)
        json_string = re.sub('"', "'", json_string)
        json_string = re.sub(r"(\w)'(\w)", r"\1\'\2", json_string)

        clean_dict = dict()
        for key, value in data_format.items():
            pattern = ''
            if isinstance(value, str):
                pattern = f"'{key}':" + "\s*'(.*?)'"
            elif isinstance(value, list):
                pattern = f"'{key}':\s*(\[[^\[\]]*?\])"
            elif isinstance(value, dict):
                pattern = f"'{key}':" + "\s*(\{[^{}]*?\})"

            extracted_value = self.extract_value(pattern, json_string)

            if extracted_value:
                try:
                    extracted_value = ast.literal_eval(extracted_value)
                except Exception:
                    pass

            if not isinstance(extracted_value, type(value)):
                extracted_value = data_format[key]
            clean_dict[key] = extracted_value

        return clean_dict

    def extract_value(self, pattern, string):
        match = re.search(pattern, string)

        if match:
            return match.group(1)
        else:
            return ''

    def clean_section_response(self, input_string):
        try:
            input_string = re.sub('^\W*"', "", input_string)
            input_string = re.sub('"\W*$', "", input_string)
        except ValueError:
            pass
        input_string = self.remove_prefix(input_string)
        return input_string

    @staticmethod
    def remove_prefix(input_string):
        return re.sub(r'\w+:\n', '', input_string)
