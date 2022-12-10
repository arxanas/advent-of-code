from dataclasses import dataclass
import os
import sys

import pyparsing as pp

TEST_INPUT = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0

@dataclass
class Instr:
    op: str
    args: list[str]
    dest: str

Input = Instr

def parse_input(input: str) -> Input:
    literal = pp.Word(pp.nums)
    variable = pp.Char(pp.alphas)
    instr = pp.Group(pp.Or([
        literal,
        pp.Keyword("NOT") + variable,
        variable + (pp.Keyword("AND") ^ pp.Keyword("OR")) + variable,
        variable + (pp.Keyword("RSHIFT") ^ pp.Keyword("LSHIFT")) + literal,
    ])) + "->" + variable
    grammar = instr[...]
    result = grammar.parse_string(input)
    # print(result.as_dict())
    return result


def test_parse_input() -> None:
    assert parse_input("x AND y -> x") == [Instr(op="AND", args=["x", "y"], dest="x")]


def simulate(input: Input) -> dict[str, int]:
    pass

def part1(input: Input) -> int:
    result = 0
    return result


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    result = 0
    return result


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT)) == PART_2_ANSWER


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
