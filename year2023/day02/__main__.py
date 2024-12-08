from __future__ import annotations

import re
import sys
from collections import Counter
from functools import reduce

from .. import utils as u

TEST_INPUT1 = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 8
PART_2_ANSWER = 2286

Draw = Counter[str]
Input = list[list[Draw]]


def parse_draw(draw: str) -> Draw:
    result = Counter[str]()
    for card in draw.split(", "):
        (count, color) = card.split(" ")
        result[color] += int(count)
    return result


def parse_input(input: str) -> Input:
    input_re = re.compile(r"Game (\d+): (.*)")
    result = []
    for i, line in enumerate(input.strip().splitlines()):
        m = input_re.match(line)
        assert m is not None
        assert int(m.group(1)) == i + 1
        result.append([parse_draw(d) for d in m.group(2).split("; ")])
    return result


def part1(input: Input) -> int:
    max = Counter(
        {
            "red": 12,
            "green": 13,
            "blue": 14,
        }
    )
    result = 0
    for i, game in enumerate(input):
        if all(draw <= max for draw in game):
            result += i + 1
    return result


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT1)) == PART_1_ANSWER


def part2(input: Input) -> int:
    result = 0
    for game in input:
        max_counts = reduce(lambda x, y: x | y, game)
        result += u.product_int(max_counts.values())
    return result


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT2)) == PART_2_ANSWER


def main() -> None:
    input = parse_input(sys.stdin.read())

    print("test 1:", part1(parse_input(TEST_INPUT1)))
    print("part 1:", part1(input))
    print("test 2:", part2(parse_input(TEST_INPUT2)))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
