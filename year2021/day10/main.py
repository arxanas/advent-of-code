import sys
from collections import *
from functools import *
from typing import *

TEST_INPUT = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""

CHARS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


Input = List[str]

def get_line_score(line: str) -> Optional[int]:
    stack = []
    for char in line:
        if char in CHARS:
            stack.append(char)
        elif char in POINTS:
            expected_char = CHARS[stack[-1]]
            if char == expected_char:
                stack.pop()
            else:
                return POINTS[char]
    return None


def part1(input: Input) -> str:
    score = 0
    for line in input:
        score += get_line_score(line) or 0
    return str(score)

def get_line_score2(line: str) -> Optional[List[str]]:
    stack = []
    for char in line:
        if char in CHARS:
            stack.append(char)
        elif char in POINTS:
            expected_char = CHARS[stack[-1]]
            if char == expected_char:
                stack.pop()
            else:
                return None
    return stack


def part2(input: Input) -> str:
    points2 = {
        "(": 1,
        "[": 2,
        "{": 3,
        "<": 4,
    }
    input = [x for line in input if (x := get_line_score2(line)) is not None]
    scores = []
    for stack in input:
        score = 0
        stack.reverse()
        for char in stack:
            score *= 5
            score += points2[char]
        scores.append(score)
    mid = len(scores) // 2
    result = sorted(scores)[mid]
    return str(result)


def parse_input(input: str) -> Input:
    return input.strip().splitlines()


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
