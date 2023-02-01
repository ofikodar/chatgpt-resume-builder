import ast
import json
from pathlib import Path
from typing import Dict

from revChatGPT.ChatGPT import Chatbot

from .prompts import get_prompt


class Chatgpt:
    def __init__(self, config_path):

        session_token = self.load_session_token(config_path)
        self.chatbot = Chatbot(session_token, conversation_id=None, parent_id=None)

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
        response = self.chatbot.ask(chatgpt_input, conversation_id=None, parent_id=None)
        new_resume_data = ast.literal_eval(response['message'])
        return new_resume_data

    @staticmethod
    def to_chatbot_input(parsed_resume: str) -> str:
        """
        Prepare the input for ChatGPT by replacing the resume placeholder with the parsed resume data

        Args:
            parsed_resume (str): parsed resume data in string format

        Returns:
            str: input for ChatGPT
        """
        chatgpt_input = PROMPT.replace(RESUME_PLACEHOLDER, parsed_resume)
        return chatgpt_input