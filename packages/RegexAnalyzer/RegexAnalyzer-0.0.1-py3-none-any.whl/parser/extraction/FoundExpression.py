# Oct 2021 
# Class for extraction.py

class FoundExpression:
    def __init__(self, expression: str,
                 file: str,
                 language: str,
                 line_no: int):
        self.expression = expression
        self.language = language
        self.file = file
        self.line_no = line_no