from __future__ import annotations

import sys

TEST_INPUT = """
A Y
B X
C Z
"""

Input = list[list[str]]


def parse_input(input: str) -> Input:
    return [line.split(" ") for line in input.strip().splitlines()]


def part1(input: Input) -> int:
    score = 0
    for lhs, rhs in input:
        lval = ord(lhs) - ord("A")
        rval = ord(rhs) - ord("X")
        result = (rval - lval) % 3
        score += rval + 1
        if result == 0:
            score += 3
        elif result == 1:
            score += 6
    return score


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == 15


def part2(input: Input) -> int:
    score = 0
    for lhs, rhs in input:
        lval = ord(lhs) - ord("A")
        result = (ord(rhs) - ord("X") - 1) % 3
        rval = (lval + result) % 3
        score += rval + 1
        if result == 0:
            score += 3
        elif result == 1:
            score += 6
    return score


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT)) == 12


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
