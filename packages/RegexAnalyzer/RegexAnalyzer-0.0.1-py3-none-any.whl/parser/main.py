# Builtin imports
import logging
import sys

# Internal imports
from parsing.parser import parse
import base64
from root_pb2 import *

log = logging.getLogger()


def main():
    expr_raw = sys.argv[1]
    fe_raw = base64.b64decode(expr_raw)
    fe = FoundExpresssion()
    fe.ParseFromString(fe_raw)
    r = Root()
    parse(fe, r.expression)
    r.expression.raw = fe.expression
    r.file = fe.file
    r.line_number = fe.line_number
    r.language = fe.language
    print(base64.b64encode(r.SerializeToString()).decode('utf-8'))


if __name__ == "__main__":
    main()
