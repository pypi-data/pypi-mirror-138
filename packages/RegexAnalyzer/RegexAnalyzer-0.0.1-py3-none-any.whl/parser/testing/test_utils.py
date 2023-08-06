"""
General utilities to help with testing - abstract away some of the complexities related to
protobuf, calling library functions, etc.
"""

# Builtin imports
import unittest
import logging

# Internal imports
import root_pb2  # The protobuf types
from parsing import parser
from extraction.FoundExpression import FoundExpression
import logconf

log = logging.getLogger()

_TOKEN_ATTRS = ["flag", "substitution", "quantifiermodifier", "anchor", "character", "lookaround",
                "escape", "groupref", "characterclass"]

class PatternTest:
    """
    A helper mixin class to define a pattern, and the protobuf tests it should map to,
    """
    # A mapping between patterns and the Root types they should correspond to (use make_root helper function)
    patterns = {}
    language = root_pb2.SupportedLanguage.Python
    file = "fakefile.py"
    line_no = 0

    def _not_testcase_error(self):
        raise AttributeError("PatternCase can only be used in a class which also inherits from unittest.TestCase")

    @staticmethod
    def _populate_expression(root_exp: root_pb2.Expression,
                             dest_exp: root_pb2.Expression):

        dest_exp.raw = root_exp.raw

        for tok in root_exp.tokens:
            dest_tok = dest_exp.tokens.add()
            dest_tok.token = tok.token
            dest_tok.type = tok.type
            if tok.type == root_pb2.TokenType.Flag:
                dest_tok.flag = tok.flag
            elif tok.type == root_pb2.TokenType.Substitution:
                dest_tok.substitution = tok.substitution
            elif tok.type == root_pb2.TokenType.QuantifierModifier:
                dest_tok.quantifiermodifier = tok.quantifiermodifier
            elif tok.type == root_pb2.TokenType.Anchor:
                dest_tok.anchor = tok.anchor
            elif tok.type == root_pb2.TokenType.GroupReference:
                dest_tok.groupref = tok.groupref
            elif tok.type == root_pb2.TokenType.Character:
                dest_tok.character = tok.character
            elif tok.type == root_pb2.TokenType.Lookaround:
                dest_tok.lookaround = tok.lookaround
            elif tok.type == root_pb2.TokenType.Escape:
                dest_tok.escape = tok.escape
            elif tok.type == root_pb2.TokenType.CharacterClass:
                dest_tok.characterclass = tok.characterclass
            else:
                raise ValueError(f"Token with unknown type {tok.type}")

        for exp in root_exp.expressions:
            log.debug(f"Generating deep copy of subexpression {exp.raw}")
            sub_dest_exp = dest_exp.expressions.add()
            PatternTest._populate_expression(exp, sub_dest_exp)
            log.debug(f"Finished sub expression {exp.raw}")

    @classmethod
    def gen_root(cls,
                 expression: root_pb2.Expression):
        log.debug(f"Generating deep copy of expression {expression.raw}")
        root = root_pb2.Root()
        root.file = cls.file
        root.language = cls.language
        root.line_number = cls.line_no

        PatternTest._populate_expression(expression, root.expression)
        log.debug(f"Finished {expression.raw}")
        return root

    def test_patterns(self):
        if hasattr(self, "assertTrue"):
            for raw_patt, root in self.patterns.items():
                # Generate a reasonable FoundExpression default
                fe = FoundExpression(raw_patt,
                                     self.file,
                                     self.language,
                                     self.line_no)
                # Run the FoundExpression object through the pat
                generated_pattern = parser.parse(fe)
                self.compare_expressions(root.expression, generated_pattern)
        else:
            self._not_testcase_error()

    def compare_tokens(self, first_tok: root_pb2.Token,
                       second_tok: root_pb2.Token):
        """
        Compare two Token objects
        """
        if hasattr(self, "assertEqual"):
            self.assertEqual(first_tok.token, second_tok.token)
            self.assertEqual(first_tok.type, second_tok.type)
            for attr in _TOKEN_ATTRS:
                self.assertEqual(getattr(first_tok, attr),
                                 getattr(second_tok, attr))
        else:
            self._not_testcase_error()

    def compare_expressions(self, first_exp: root_pb2.Expression,
                            second_exp: root_pb2.Expression):
        """
        Recursively compare two Expression objects
        """
        if hasattr(self, "assertEqual"):
            self.assertEqual(first_exp.raw, second_exp.raw)
            self.assertEqual(len(first_exp.tokens), len(second_exp.tokens))
            for i in range(len(first_exp.tokens)):
                self.compare_tokens(first_exp.tokens[i], second_exp.tokens[i])
            self.assertEqual(len(first_exp.expressions), len(second_exp.expressions))
            for i in range(len(first_exp.expressions)):
                self.compare_expressions(first_exp.expressions[i], second_exp.expressions[i])
        else:
            self._not_testcase_error()

    def compare_patterns(self, first_patt: root_pb2.Root,
                         second_patt: root_pb2.Root):
        """
        Compare two Root objects
        """
        if hasattr(self, "assertEqual"):
            # Go through all the attributes of a pattern, and make sure they match
            self.assertEqual(first_patt.file, second_patt.file)
            self.assertEqual(first_patt.language, second_patt.language)
            self.assertEqual(first_patt.line_number, second_patt.line_number)
            self.assertEqual(len(first_patt.expressions), len(second_patt.expressions))
            for i in range(len(first_patt.expressions)):
                self.compare_expressions(first_patt.expressions[i],
                                         second_patt.expressions[i])
        else:
            self._not_testcase_error()


