# Oct 2021 
# Functions for the Java parts of extraction.py 

# NOTE: 
# Doesn't catch the extra info in cases like "Pattern.compile("ge*", Pattern.CASE_INSENSITIVE)"
# Also might want to modify to check for "import java.util.regex.Matcher;"
#   and then Pattern.compile 


# Builtin import
from typing import Generator

# Internal import 
try:
    from extraction.FoundExpression import FoundExpression
except ImportError:
    from FoundExpression import FoundExpression


def line_scan(line: str):
    """
    Call this on a line of Java code, get out regex

    :param line: A line of Java code 
    :return: A regex string or None 
    """

    # all the function calls containing regexes (maybe) 
    functions = ["compile", "matches"]

    for func in functions:
        if func in line:
            # start and end index of exp
            start = line.index(func) + len(func) + 1 # 1 from open paren
            end = len(line)-1
            for i, chr in enumerate(line):
                # if it's a closing quote 
                # and you haven't found it yet)
                # and it's not escaped 
                if i > start and chr == line[start] and end == len(line)-1 and line[i-1] != "\\":
                    end = i 
            regex = line[start+1:end]
            return regex

        else: 
            return None 


def extract_java(fpath: str):
    """
    Extract regexes from java file

    :param fpath: A path to a file 
    :return: A list of FoundExpressions 
    """

    # find import statement 
    f = open(fpath, "r")
    # get lines in file 
    lines = f.readlines()
    expressions = [] # list of FoundExpressions 
    imported = [] # imported funcs 

    for line_no, line in enumerate(lines):
        regex = line_scan(line) 
        if regex != None: 
            expressions.append(FoundExpression(regex, fpath, "Java", line_no))
    
    return expressions 