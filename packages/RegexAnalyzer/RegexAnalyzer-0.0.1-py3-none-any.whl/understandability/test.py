import root_pb2
import base64
import json
from understandability import analyze
from google.protobuf.json_format import MessageToJson, MessageToDict

test_S1S3L1 = root_pb2.Expression(
            raw='S{3}S{4,4}S{7,7}A{2,}',
            tokens=[
  root_pb2.Token(
    token="S",
    type=root_pb2.TokenType.Character,
    character="S"
    ),
  root_pb2.Token(
    token="{3}",
    type=root_pb2.TokenType.QuantifierModifier,
    quantifiermodifier=root_pb2.QuantifierModifierType.SpecifiedQuantifier
    ),
  root_pb2.Token(
    token="S",
    type=root_pb2.TokenType.Character,
    character="S"
    ),
  root_pb2.Token(
    token="{4,4}",
    type=root_pb2.TokenType.QuantifierModifier,
    quantifiermodifier=root_pb2.QuantifierModifierType.SpecifiedQuantifier
    ),
  root_pb2.Token(
    token="S",
    type=root_pb2.TokenType.Character,
    character="S"
    ),
  root_pb2.Token(
    token="{7,7}",
    type=root_pb2.TokenType.QuantifierModifier,
    quantifiermodifier=root_pb2.QuantifierModifierType.SpecifiedQuantifier
    ),
  root_pb2.Token(
    token="A",
    type=root_pb2.TokenType.Character,
    character="S"
    ),
  root_pb2.Token(
    token="{2,}",
    type=root_pb2.TokenType.QuantifierModifier,
    quantifiermodifier=root_pb2.QuantifierModifierType.SpecifiedQuantifier
    ),
],
        )
ans_S1S3L1 = {"status": "4 understandability errors found","annotations": [{"note": "SSS","entity": "S{3}"},{"note": "SSSS","entity": "S{4,4}"},{"note": "S{7}","entity": "S{7,7}"},{"note": "AA+","entity": "A{2,}"}]}

test_L2 = root_pb2.Expression(
            raw='AAA*',
            tokens=[
  root_pb2.Token(
    token="AAA",
    type=root_pb2.TokenType.Character,
    character="AAA"
    ),
  root_pb2.Token(
    token="*",
    type=root_pb2.TokenType.QuantifierModifier,
    quantifiermodifier=root_pb2.QuantifierModifierType.Star
    ),
],)
ans_L2 = {'status': '1 understandability error found', 'annotations': [{'note': 'AA+', 'entity': 'AAA*'}]}

test_T2T4 = root_pb2.Expression(
            raw='\\x61\\141',
            tokens=[
  root_pb2.Token(
    token="\\x61",
    type=root_pb2.TokenType.Escape,
    escape=root_pb2.EscapeType.Hexadecimal
    ),
  root_pb2.Token(
    token="\\141",
    type=root_pb2.TokenType.Escape,
    escape=root_pb2.EscapeType.Octal
    ),
],)
ans_T2T4 = {'status': '2 understandability errors found', 'annotations': [{'note': 'a', 'entity': '\\x61'}, {'note': 'a', 'entity': '\\141'}]}

test_Set = root_pb2.Expression(
            raw='[0-9][^\\s][$][aaa]',
            tokens=[
  root_pb2.Token(
    token="[",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.OpenSet
    ),
  root_pb2.Token(
    token="0-9",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.RangeSet
    ),
  root_pb2.Token(
    token="]",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.CloseSet
    ),
  root_pb2.Token(
    token="[",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.OpenSet
    ),
  root_pb2.Token(
    token="^",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.SetNegation
    ),
  root_pb2.Token(
    token="\\s",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.Whitespace
    ),
  root_pb2.Token(
    token="]",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.CloseSet
    ),
  root_pb2.Token(
    token="[",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.OpenSet
    ),
  root_pb2.Token(
    token="$",
    type=root_pb2.TokenType.Character,
    character="$"
    ),
  root_pb2.Token(
    token="]",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.CloseSet
    ),
  root_pb2.Token(
    token="[",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.OpenSet
    ),
  root_pb2.Token(
    token="aaa",
    type=root_pb2.TokenType.Character,
    character="aaa"
    ),
  root_pb2.Token(
    token="]",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.CloseSet
    ),
],)
ans_Set = {'status': '4 understandability errors found', 'annotations': [{'note': '\\d', 'entity': '[0-9]'}, {'note': '\\S', 'entity': '[^\\s]'}, {'note': '\\$', 'entity': '[$]'}, {'note': 'repeated characters in []', 'entity': '[aaa]'}]}

test_SetT2T4 = root_pb2.Expression(
            raw='\\x61\\141',
            tokens=[
  root_pb2.Token(
    token="[",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.OpenSet
    ),
  root_pb2.Token(
    token="\\x61",
    type=root_pb2.TokenType.Escape,
    escape=root_pb2.EscapeType.Hexadecimal
    ),
  root_pb2.Token(
    token="\\141",
    type=root_pb2.TokenType.Escape,
    escape=root_pb2.EscapeType.Octal
    ),
  root_pb2.Token(
    token="]",
    type=root_pb2.TokenType.CharacterClass,
    characterclass=root_pb2.CharacterClassType.CloseSet
    ),
],)
ans_SetT2T4 = {'status': '2 understandability errors found', 'annotations': [{'note': 'a', 'entity': '\\x61'}, {'note': 'a', 'entity': '\\141'}]}

test_TooLong = root_pb2.Expression(
            raw='([A-Z])\w+([A-Z])\w+([A-Z])\w+([A-Z])\w+([A-Z])\w+([A-Z])\w+([A-Z])\w+([A-Z])\w+([A-Z])\w+([A-Z])\w+([A-Z])\w+([A-Z])\w+([A-Z])\w+',
            tokens=[],)
ans_TooLong = {'status': '1 understandability error found', 'annotations': [{'note': 'rejex is too long. Limit rejex to 128 characters', 'entity': '([A-Z])\\w+([A-Z])\\w+([A-Z])\\w+([A-Z])\\w+([A-Z])\\w+([A-Z])\\w+([A-Z])\\w+([A-Z])\\w+([A-Z])\\w+([A-Z])\\w+([A-Z])\\w+([A-Z])\\w+([A-Z])\\w+'}]}

def test(t, ans):
  expr_raw = base64.b64decode(base64.b64encode(t.SerializeToString()).decode('utf-8'))
  expr = root_pb2.Expression()
  expr.ParseFromString(expr_raw)
  output = root_pb2.Output()
  analyze(expr.tokens, output, expr.raw)
  if len(output.annotations) <= 1:
    output.status = str(len(output.annotations)) + " understandability error found"
  else:
    output.status = str(len(output.annotations)) + " understandability errors found"
  # print(MessageToDict(output))
  json1 = json.dumps(ans, sort_keys=True)
  json2 = json.dumps(MessageToDict(output), sort_keys=True)
  return json1 == json2

def main():
  print(test(test_S1S3L1, ans_S1S3L1))
  print(test(test_L2, ans_L2))
  print(test(test_T2T4, ans_T2T4))
  print(test(test_Set, ans_Set))
  print(test(test_SetT2T4, ans_SetT2T4))
  print(test(test_TooLong, ans_TooLong))

if __name__ == "__main__":
  main()

  