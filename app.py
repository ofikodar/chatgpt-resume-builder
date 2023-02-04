from src.ui import *
from src.utils import is_chatbot_loaded


def main():
    title()
    if is_chatbot_loaded():
        sidebar()

        if is_data_loaded():
            header()
            body()

        else:
            upload_resume_header()
    else:
        init_chatbot()


if __name__ == '__main__':
    main()
