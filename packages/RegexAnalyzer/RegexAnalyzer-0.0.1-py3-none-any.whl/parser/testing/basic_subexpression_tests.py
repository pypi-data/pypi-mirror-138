
# Builtin imports
import unittest
import logging

# Internal imports
import root_pb2
from testing.test_utils import PatternTest
import logconf


class BasicSubexpressionTests(unittest.TestCase,
                              PatternTest):
    patterns = {
        "{.*}": PatternTest.gen_root(root_pb2.Expression(
            raw='{.*}',
            tokens=[
                # Add tokens here
                root_pb2.Token(
                    token="{",
                    type=root_pb2.TokenType.Character,
                    character="{"
                ),
                root_pb2.Token(
                    token=".",
                    type=root_pb2.TokenType.CharacterClass,
                    characterclass=root_pb2.CharacterClassType.Dot
                ),
                root_pb2.Token(
                    token="*",
                    type=root_pb2.TokenType.QuantifierModifier,
                    quantifiermodifier=root_pb2.QuantifierModifierType.Star
                ),
                root_pb2.Token(
                    token="}",
                    type=root_pb2.TokenType.Character,
                    character="}"
                ),
            ],
            expressions=[
                root_pb2.Expression(
                    raw="{",
                    tokens=[
                        root_pb2.Token(
                            token="{",
                            type=root_pb2.TokenType.Character,
                            character="{"
                        ),
                    ]
                ),
                root_pb2.Expression(
                    raw=".*",
                    tokens=[
                        root_pb2.Token(
                            token=".",
                            type=root_pb2.TokenType.CharacterClass,
                            characterclass=root_pb2.CharacterClassType.Dot
                        ),
                        root_pb2.Token(
                            token="*",
                            type=root_pb2.TokenType.QuantifierModifier,
                            quantifiermodifier=root_pb2.QuantifierModifierType.Star
                        ),
                    ]
                ),
                root_pb2.Expression(
                    raw="}",
                    tokens=[
                        root_pb2.Token(
                            token="}",
                            type=root_pb2.TokenType.Character,
                            character="}"
                        ),
                    ]
                ),
            ]
        )),
        r"/[\d\.]/": PatternTest.gen_root(root_pb2.Expression(
            raw=r'/[\d\.]/',
            tokens=[
                # Add tokens here
                root_pb2.Token(
                    token=r"/",
                    type=root_pb2.TokenType.Character,
                    character="/"
                ),
                root_pb2.Token(
                    token="[",
                    type=root_pb2.TokenType.CharacterClass,
                    characterclass=root_pb2.CharacterClassType.OpenSet
                ),
                root_pb2.Token(
                    token=r"\d",
                    type=root_pb2.TokenType.CharacterClass,
                    characterclass=root_pb2.CharacterClassType.Digit
                ),
                root_pb2.Token(
                    token=r"\.",
                    type=root_pb2.TokenType.Escape,
                    escape=root_pb2.EscapeType.Reserved
                ),
                root_pb2.Token(
                    token="]",
                    type=root_pb2.TokenType.CharacterClass,
                    characterclass=root_pb2.CharacterClassType.CloseSet
                ),
                root_pb2.Token(
                    token="/",
                    type=root_pb2.TokenType.Character,
                    character="/"
                ),
            ],
            expressions=[
                root_pb2.Expression(
                    raw='/',
                    tokens=[
                        root_pb2.Token(
                            token=r"/",
                            type=root_pb2.TokenType.Anchor,
                            anchor=root_pb2.AnchorType.ForwardSlash
                        ),
                    ]
                ),
                root_pb2.Expression(
                    raw=r'[\d\.]',
                    tokens=[
                        root_pb2.Token(
                            token="[",
                            type=root_pb2.TokenType.CharacterClass,
                            characterclass=root_pb2.CharacterClassType.OpenSet
                        ),
                        root_pb2.Token(
                            token=r"\d",
                            type=root_pb2.TokenType.Character,
                            characterclass=root_pb2.CharacterClassType.Digit
                        ),
                        root_pb2.Token(
                            token=r"\.",
                            type=root_pb2.TokenType.Escape,
                            characterclass=root_pb2.EscapeType.Reserved
                        ),
                        root_pb2.Token(
                            token="]",
                            type=root_pb2.TokenType.CharacterClass,
                            characterclass=root_pb2.CharacterClassType.CloseSet
                        ),
                    ]
                ),
                root_pb2.Expression(
                    raw='/',
                    tokens=[
                        root_pb2.Token(
                            token="/",
                            type=root_pb2.TokenType.Anchor,
                            anchor=root_pb2.AnchorType.ForwardSlash
                        ),
                    ]
                )
            ]
        ))
    }