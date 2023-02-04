from revChatGPT.Official import Chatbot

from src.chatbot.chatgpt import Chatgpt

if __name__ == '__main__':
    chatbot = Chatgpt('config.json')
    y = chatbot.improve_section('My name is ofek i have an msc i lead NLP projects')
    print(y)

