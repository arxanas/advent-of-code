from collections import Counter
import re
from typing import Literal, Union


def split_line_groups(input: str) -> list[str]:
    """Split the input into groups of lines separated by blank lines."""
    return input.strip().split("\n\n")


AutoparsedInput = Union[list[int], list["AutoparsedInput"]]


def autoparse_input(input: str) -> AutoparsedInput:
    """Attempt to parse the input into an intelligent structure."""
    groups: list[list[list[Token]]] = []
    for group_text in input.strip().split("\n\n"):
        groups.append([])
        for line_text in group_text.strip().split("\n"):
            groups[-1].append(tokenize(line_text))

    token_counter = Counter(
        token for group in groups for line in group for token in line
    )
    most_common_tokens = token_counter.most_common()
    average_token_count = sum(j for (_, j) in most_common_tokens) / len(
        most_common_tokens
    )
    common_tokens = {
        token for (token, count) in most_common_tokens if count >= average_token_count
    }
    # uncommon_tokens = [token for (token, count) in most_common_tokens if count < average_token_count]

    record_schema_set = set()
    for group in groups:
        for line in group:
            tokens = tuple(token for token in line if token in common_tokens)
            record_schema_set.add(tokens)
    record_schema = sorted(list(record_schema_set))

    def find_matching_schema(line: list[Token]) -> list[Token]:
        for schema in record_schema:
            for (lhs, rhs) in zip(line, schema):
                if lhs is not None and rhs != lhs:
                    break
            else:
                return list(schema)
        raise ValueError(f"No matching schema for line {line!r}")

    result = []
    for group in groups:
        for line in group:
            schema = find_matching_schema(line)


def unify(schemas: list[list[Token]]) -> list[SchemaToken]:
    ...


TypeHint = Union[Literal["int"], Literal["str"], Literal["punct"]]
Token = tuple[str, TypeHint]
SchemaToken = Union[tuple[Literal["binding"], Token], tuple[Literal["static"], Token]]


def tokenize(line: str) -> list[Token]:
    """Analyze the tokens and return a list of strings describing them."""
    result = []
    token_re = re.compile(
        r"""
        (?P<int>\d+) |
        (?P<str>[a-zA-Z]+) |
        (?P<punct>[^\w \r\n]+)
        """,
        re.VERBOSE,
    )
    for match in token_re.finditer(line.strip()):
        hint: TypeHint
        if (value := match.group("int")) is not None:
            hint = "int"
        elif (value := match.group("str")) is not None:
            hint = "str"
        elif (value := match.group("punct")) is not None:
            hint = "punct"
        else:
            raise RuntimeError("Unexpected matches: {!r}".format(match.groupdict()))
        result.append((value, hint))
    return result


def test_tokenize() -> None:
    assert tokenize("Monkey 0: 79, 98") == [
        ("Monkey", "str"),
        ("0", "int"),
        (":", "punct"),
        ("79", "int"),
        (",", "punct"),
        ("98", "int"),
    ]


def test_autoparse() -> None:
    """Test the autoparser."""
    input = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
    expected = [
        (0, [79, 98], "* 19", 23, 2, 3),
        (1, [54, 65, 75, 74], "+ 6", 19, 2, 0),
        (2, [79, 60, 97], "* old", 13, 1, 3),
        (3, [74], "+ 3", 17, 0, 1),
    ]
    assert autoparse_input(input) == expected
