from __future__ import annotations

import re
import sys

TEST_INPUT1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

TEST_INPUT2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

PART_1_ANSWER = 142
PART_2_ANSWER = 281

Input = list[str]


def parse_input(input: str) -> Input:
    return input.strip().splitlines()


def part1(input: Input) -> int:
    nums = []
    for line in input:
        digits = [c for c in line if c.isdigit()]
        nums.append(int(digits[0] + digits[-1]))
    return sum(nums)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT1)) == PART_1_ANSWER


def part2(input: Input) -> int:
    digit_re = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))")
    digits_map = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    def parse_digit(digit: str) -> str:
        if digit.isdigit():
            return digit
        else:
            return digits_map[digit]

    nums = []
    for line in input:
        digits = [m.group(1) for m in digit_re.finditer(line)]
        num_str = parse_digit(digits[0]) + parse_digit(digits[-1])
        nums.append(int(num_str))

    return sum(nums)


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT2)) == PART_2_ANSWER


def test_overlapping_digits() -> None:
    assert part2(parse_input("oneight")) == 18


def main() -> None:
    input = parse_input(sys.stdin.read())

    print("test 1:", part1(parse_input(TEST_INPUT1)))
    print("part 1:", part1(input))
    print("test 2:", part2(parse_input(TEST_INPUT2)))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
