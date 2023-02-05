from src.ui import *
from src.utils import is_chatbot_loaded


def main():
    title()
    try:
        if is_chatbot_loaded():
            sidebar()

            if is_data_loaded():
                resume_header()
                body()
            else:
                user_info()
        else:
            init_chatbot()
    except:
        unknown_error()


if __name__ == '__main__':
    main()
