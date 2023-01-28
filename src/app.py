import os
import argparse

from src.chatbot.chatgpt import Chatgpt
from src.utils import parse_pdf, export_html_resume


def parse_and_improve_resume(args):
    input_path = os.path.join(args.data_dir, args.input_resume)
    parsed_resume = parse_pdf(input_path)

    chatbot = Chatgpt()
    new_resume_data = chatbot.improve_resume(parsed_resume)

    output_path = os.path.join(args.data_dir, args.output_file)
    export_html_resume(new_resume_data, output_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default='../data', help="Directory containing input and output files")
    parser.add_argument("--input_resume", type=str, default='example_input.pdf', help="Name of input resume file")
    parser.add_argument("--output_resume", type=str, default='new_resume.html', help="Name of output resume file")
    args = parser.parse_args()

    parse_and_improve_resume(args)


if __name__ == '__main__':
    main()
