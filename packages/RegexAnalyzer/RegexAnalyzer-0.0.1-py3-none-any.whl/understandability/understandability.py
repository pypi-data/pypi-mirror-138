import root_pb2 as root
import re
import sys
import base64
from google.protobuf.json_format import MessageToDict
import json

escape_reserved = ['+', '*', '?', '^', '$', '\\', '.', '[', ']', '{', '}', '(', ')', '|', '/']
messages = []


def add_annotation(entity, note, output):
    annotation = output.annotations.add()
    annotation.note = note
    annotation.entity = entity


# Analyze understandability of []
def analyze_set(tokens, output):
    set_string = "["
    set_messages = []
    characters = []  # what is in set
    for i in range(len(tokens)):
        set_string += tokens[i].token
        if tokens[i].token == "]" and tokens[1].type == root.TokenType.CharacterClass:
            # \d better than [0-9]
            if i == 1 and tokens[0].type == root.TokenType.CharacterClass and \
                    tokens[0].characterclass == root.CharacterClassType.RangeSet and tokens[0].token == "0-9":
                add_annotation("[0-9]", "\\d", output)
            # \D better than [^\d], \S better than [^\s], \W better than [^\w]
            if i == 2 and tokens[0].type == root.TokenType.CharacterClass and \
                    tokens[0].characterclass == root.CharacterClassType.SetNegation and \
                    tokens[1].type == root.TokenType.CharacterClass and \
                    (tokens[1].characterclass == root.CharacterClassType.Digit or \
                     tokens[1].characterclass == root.CharacterClassType.Word or \
                     tokens[1].characterclass == root.CharacterClassType.Whitespace):
                add_annotation("[^" + tokens[1].token + "]", "\\" + tokens[1].token[-1].upper(), output)
            # T3 \$ better than [$] -- T3
            if i == 1 and tokens[0].token in escape_reserved:
                add_annotation("[" + tokens[0].token + "]", "\\" + tokens[0].token, output)
            # [aaabbb] is equivalent to [ab]
            if len(set(characters)) != len(characters):
                add_annotation(set_string, "repeated characters in []", output)
            return set_messages, i + 1
        # [}{] better than [\0175\0173]
        # T2 and T4 (repetitive but no better solution for now)
        if tokens[i].type == root.TokenType.Escape:
            if tokens[i].escape == root.EscapeType.Hexadecimal:
                char = bytearray.fromhex(tokens[i].token[-2:]).decode('unicode-escape')
            elif tokens[i].escape == root.EscapeType.Octal:
                char = tokens[i].token.encode('utf-8').decode('unicode-escape')
            else:
                char = ""
            if char and char in escape_reserved:
                add_annotation(tokens[i].token, "\\" + char, output)
            elif char:
                add_annotation(tokens[i].token, char, output)
        if tokens[i].type == root.TokenType.Character:
            characters.extend(list(tokens[i].token))
        else:
            characters.append(tokens[i].token)
    return set_messages, i + 1


def analyze(tokens, output, raw):
    # regular expression is limited to 128 characters
    if len(raw) > 128:
        add_annotation(raw, "rejex is too long. Limit rejex to 128 characters", output)
    i = 0
    while i < len(tokens):
        token = tokens[i]
        # print(token)
        if i >= 1 and token.type == root.TokenType.QuantifierModifier and \
                token.quantifiermodifier == root.QuantifierModifierType.SpecifiedQuantifier:
            # S1
            if token.token[1:-1].isdigit() and int(token.token[1:-1]) < 6:
                add_annotation(tokens[i - 1].token + token.token, tokens[i - 1].token * int(token.token[1:-1]), output)
            else:
                # S3
                # S{7,7} should be S{7}
                # S{3,3} should be SSS
                nums = re.findall("\d", token.token[1:-1])
                if len(nums) == 2 and nums[0] == nums[1]:
                    if int(nums[0]) < 6:
                        add_annotation(tokens[i - 1].token + token.token, tokens[i - 1].token * int(nums[0]), output)
                    else:
                        add_annotation(tokens[i - 1].token + token.token,
                                       tokens[i - 1].token + "{" + str(nums[0]) + "}", output)
                # L1
                if len(nums) == 1 and int(nums[0]) < 5:
                    add_annotation(tokens[i - 1].token + token.token, tokens[i - 1].token * int(nums[0]) + "+", output)
        # L2
        if token.type == root.TokenType.QuantifierModifier and \
                token.quantifiermodifier == root.QuantifierModifierType.Star:
            if i - 1 >= 0 and tokens[i - 1].type == root.TokenType.Character and len(tokens[i - 1].token) >= 2 and \
                    tokens[i - 1].token[-1] == tokens[i - 1].token[-2]:
                add_annotation(tokens[i - 1].token + token.token, tokens[i - 1].token[:-1] + "+", output)
        # T2 and T4
        if token.type == root.TokenType.Escape:
            if token.escape == root.EscapeType.Hexadecimal:
                char = bytearray.fromhex(token.token[-2:]).decode('unicode-escape')
            elif token.escape == root.EscapeType.Octal:
                char = token.token.encode('utf-8').decode('unicode-escape')
            else:
                char = ""
            if char and char in escape_reserved:
                add_annotation(token.token, "\\" + char, output)
            elif char:
                add_annotation(token.token, char, output)
        # []
        if token.type == root.TokenType.CharacterClass and \
                token.characterclass == root.CharacterClassType.OpenSet:
            set_messages, length = analyze_set(tokens[i + 1:], output)
            i += length - 1  # += 1 later
        i += 1


# https://www.dcode.fr/regular-expression-simplificator
# Get some ideas from here
# https://help.analyticsedge.com/error/400-regular-expression-too-long/
# Got some ideas about regex length

def main():
    expr_raw = base64.b64decode(sys.argv[1])
    expr = root.Expression()
    expr.ParseFromString(expr_raw)
    output = root.Output()
    analyze(expr.tokens, output, expr.raw)
    if len(output.annotations) <= 1:
        output.status = str(len(output.annotations)) + " understandability error found"
    else:
        output.status = str(len(output.annotations)) + " understandability errors found"
    print(base64.b64encode(output.SerializeToString()).decode('utf-8'))


if __name__ == "__main__":
    main()
