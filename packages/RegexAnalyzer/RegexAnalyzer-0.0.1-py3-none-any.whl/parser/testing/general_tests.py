"""
A test for some of the general and basic cases that will come up parsing regular expressions -
we'll want to have one of these files for each "topic", for ex. maybe one as well like
lookaround_test.py where we have a few tests related to lookarounds.
Each of these should define a few test cases that broadly cover the topic. We're aiming
for 100% test coverage, which means that every line of code in the repository is at some
point read by the app
"""

# Builtin imports
import unittest
import logging

# Internal imports
import root_pb2
from testing.test_utils import PatternTest
import logconf


class TestBasicPatterns(unittest.TestCase,
                        PatternTest):
    patterns = {
        r'\W+': PatternTest.gen_root(root_pb2.Expression(
            raw=r'\W+',
            tokens=[
                # Add tokens here
                root_pb2.Token(
                    token=r"\W",
                    type=root_pb2.TokenType.CharacterClass,
                    characterclass=root_pb2.CharacterClassType.NotWord
                ),
                root_pb2.Token(
                    token=r"+",
                    type=root_pb2.TokenType.QuantifierModifier,
                    quantifiermodifier=root_pb2.QuantifierModifierType.Plus
                ),
            ],
            expressions=[
                # Add any subexpressions here
            ]
        )),
        "^window._sharedData": PatternTest.gen_root(root_pb2.Expression(
            raw="^window._sharedData",
            tokens=[
                # Add tokens here
                root_pb2.Token(
                    token="^",
                    type=root_pb2.TokenType.Anchor,
                    anchor=root_pb2.AnchorType.Beginning
                ),
                root_pb2.Token(
                    token="window",
                    type=root_pb2.TokenType.Character,
                    character="window"
                ),
                root_pb2.Token(
                    token=".",
                    type=root_pb2.TokenType.CharacterClass,
                    characterclass=root_pb2.CharacterClassType.Dot
                ),
                root_pb2.Token(
                    token="_sharedData",
                    type=root_pb2.TokenType.Character,
                    character="_sharedData"
                ),
            ],
            expressions=[
                # Add any subexpressions here
            ]
        ))
    }
