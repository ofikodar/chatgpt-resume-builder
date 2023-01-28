import json

import gradio as gr
from src.utils import parse_pdf, build_html_resume


def process_pdf(pdf_file):
    html_resume = build_html_resume(json.load(open(pdf_file.name)))

    return html_resume

def _app():
    demo = gr.Interface(
        process_pdf,
        gr.inputs.File(),
        "html"
    )
    demo.launch()




if __name__ == '__main__':
    _app()
