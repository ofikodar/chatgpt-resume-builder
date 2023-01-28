import ast
import json

from revChatGPT.ChatGPT import Chatbot

from src.chatbot.prompts import PROMPT, RESUME_PLACEHOLDER


class Chatgpt:
    def __init__(self):
        session_token = self.load_session_token()
        self.chatbot = Chatbot(session_token, conversation_id=None,
                               parent_id=None)  # You can start a custom conversation

    @staticmethod
    def load_session_token():
        with open('config.json', 'r') as j_file:
            session_token = json.load(j_file)
        return session_token

    def improve_resume(self, parsed_resume):
        chatgpt_input = self.to_chatbot_input(parsed_resume)
        response = self.chatbot.ask(chatgpt_input, conversation_id=None,
                                    parent_id=None)
        new_resume_data = ast.literal_eval(response['message'])
        return new_resume_data

    @staticmethod
    def to_chatbot_input(parsed_resume):
        chatgpt_input = PROMPT.replace(RESUME_PLACEHOLDER, parsed_resume)
        return chatgpt_input
