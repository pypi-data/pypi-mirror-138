# Oct 2021 
# Functions for the Python parts of extraction.py 

# NOTE: 
# Currently only finds a single regex per line 
# Also only finds regexes attached to functions in the "functions" list 
# And assumes the regex is their first argument 

# Builtin import
from typing import Generator
import re

# Internal import
try:
    from extraction.FoundExpression import FoundExpression
except ImportError:
    from FoundExpression import FoundExpression

# A pattern that we'll use to determine if the regex library has been imported
import_patt = re.compile(r'(?:import|from) re(?:\n|(?: import)?)(?: as (.*))?')
# The valid functions to come after re.
_SUPPORTED_FUNCTIONS = [
    "compile",
    "search",
    "match",
    "fullmatch",
    "split",
    "findall",
    "finditer",
    "sub"
]


def extract_py(fpath: str):
    """
    Extract regexes from python file

    :param fpath: A path to a file 
    :return: A list of FoundExpressions 
    """
    expressions = []
    with open(fpath) as fopen:
        fdata = fopen.read()
        # Check to see if we can find a usable regex import in the file
        match = import_patt.match(fdata)
        if match:
            alternate_import = match.groups()[0]
            # If there was an 'import re as x' line, the matching group in the pattern will pull that out here -
            # otherwise, we're looking for something that starts with re.
            import_name = alternate_import if alternate_import else 're'
            # Monstrous pattern to match the valid usages of regular expressions in the code -
            # step by step -
            combined_patt = fr'[^#\n]*{import_name}\.({"|".join(_SUPPORTED_FUNCTIONS)})([ \n\t])*\((?:[ \n\tf])*(?:r)?([\'"])(.*)([^\\])\3'
            patt_matches = re.findall(combined_patt, fdata)
            # patt_matches = re.findall(
            #     #  Don't match anything that's a comment, and don't allow run-on to newlines
            #     fr'[^#\n]*' +
            #     #  The name of the library we're matching (either re or import re as *) + the '.' character
            #     fr'{import_name}\.' +
            #     # One of our supported regex functions (compile, search, etc.), in a non-capturing group
            #     fr'(?:{"|".join(_SUPPORTED_FUNCTIONS)})' +
            #     # Allow newlines, tabs, and spaces between the function call and the opening paren
            #     r'(?:[ \n\t])*\(' +
            #     # Allow the same, plus the "f" character, for f-regex strings (like this one), before the
            #     # beginning of the actual regex string. Then, allow the string to start with the r for raw
            #     # literal, and either a # single or double quote
            #     r'(?:[ \n\tf])*(?:r)?([\'"])' +
            #     # Finally, match the actual pattern, and make sure we close with the same type of quote
            #     # we opened with by making a backreference to our quote group
            #     r'(.*)(?:[^\\]\3)'
            #     , fdata)
            if patt_matches:
                for match in patt_matches:
                    # Escape backslashes
                    found_pattern = ''.join(match[3:]).replace('\\\\', '\\')
                    expressions.append(
                        FoundExpression(
                            found_pattern,
                            fpath,
                            "Python",
                            0 # TODO: Gen line number,
                        )
                    )

    return expressions
