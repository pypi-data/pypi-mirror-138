"""
Helper script, for directly testing the parser
"""
import sys
from extraction.FoundExpression import FoundExpression
from parsing.parser import parse
import base64


def main(expr: FoundExpression):
    print(base64.b64encode(parse(expr).SerializeToString()).decode('utf-8'))

if __name__ == "__main__":
    main(FoundExpression(expression=sys.argv[1], line_no=1, language="Python", file="fake.py"))