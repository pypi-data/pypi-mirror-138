# Oct 18 2021 
# Extract regex strings from project files 

# NOTE: 
# Currently totally missing things like: 
    # String pattern = "(.*)(\\d+)(.*)";
    # Pattern r = Pattern.compile(pattern);
# Helpful links to docs: 
    # https://blog.teamtreehouse.com/regular-expressions-10-languages


# Builtin import
import os
from typing import Generator

# Internal import 
try:
    from extraction.FoundExpression import FoundExpression
    from extraction.extraction_py import extract_py
    from extraction.extraction_java import extract_java
except ImportError:
    from extraction_py import extract_py
    from extraction_java import extract_java
# from extraction_js import extract_js 
# from extraction_rb import extract_rb


def find_files(dir_name):
    """
    :param dir_name: The directory to search for regular expressions in
    :return: A list of filenames in the given directory 
    """
    return os.listdir(dir_name)


def extract_regex(fname: str):
    """
    Direct files to language-specific extraction functions 

    :param fname: A filename 
    """
    ext = fname.split(".")[-1]
    if ext == "py":
        return extract_py(fname)
    elif ext == "java":
        return extract_java(fname) 
    # elif ext in ["js", "ts", "jsx", "tsx"]:
    #     return extract_js(fname)
    # elif ext in ["rs", "rlib"]:
    #     return extract_rust(fname)
    # elif ext == "go":
    #     return extract_go(fname)
    # elif ext == "php":
    #     return extract_php(fname)
    # elif ext == "rb":
    #     return extract_rb(fname)


def extract(dir_name):
    """
    Given a particular directory, yield all the regular expressions that can be found in it

    :param dir_name: The directory to search for regular expressions in
    :return: A generator of FoundExpression objects
    """

    for fname in find_files(dir_name):
        fpath = os.path.join(dir_name, fname)
        if os.path.isdir(fpath):
            yield from extract(fpath)
        else:
            expressions = extract_regex(fpath)
            if expressions:
                for exp in expressions:
                    yield exp # exp.expression, exp.language, exp.line_no


if __name__ == "__main__":
    dir_name = "testing"
    for i in extract(dir_name):
        print("OUT:", i.expression)
