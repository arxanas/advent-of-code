import sys

from .. import utils

TEST_INPUT = """
mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""

PART_1_ANSWER = 7
PART_2_ANSWER = 19

Input = str


def parse_input(input: str) -> Input:
    return input.strip()


def part1(input: Input) -> int:
    for i in range(4, len(input)):
        last_four = input[i - 4 : i]
        if utils.all_different(last_four):
            return i
    raise ValueError("Start of packet not found")


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    for i in range(14, len(input)):
        last_fourteen = input[i - 14 : i]
        if utils.all_different(last_fourteen):
            return i
    raise ValueError("Start of message not found")


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
