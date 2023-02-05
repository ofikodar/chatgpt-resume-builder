class PDFSizeException(Exception):
    """Raised when the input value is less than 3"""
    pass


class ChatbotInitException(Exception):
    """Raised when there's a problem with chabot init"""
    pass


class ChatbotAPIException(Exception):
    """Raised when there's a problem with openai api"""
    pass
