import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

TEST_INPUT = """
TODO
"""

PART_1_ANSWER = 0
PART_2_ANSWER = 0

Input = str


def parse_input(input: str) -> Input:
    return input


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
