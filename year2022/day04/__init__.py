import sys

from .. import utils

TEST_INPUT = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

PART_1_ANSWER = 2
PART_2_ANSWER = 4

Input = list[list[tuple[int, int]]]


def parse_input(input: str) -> Input:
    result = []
    for line in input.strip().splitlines():
        pair = []
        for section in line.split(","):
            lhs, rhs = section.split("-")
            pair.append((int(lhs), int(rhs)))
        result.append(pair)
    return result


def part1(input: Input) -> int:
    result = 0
    for (lhs, rhs) in input:
        lhs2 = utils.InclusiveInterval.from_tuple(lhs)
        rhs2 = utils.InclusiveInterval.from_tuple(rhs)
        if lhs2 in rhs2 or rhs2 in lhs2:
            result += 1
    return result


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    result = 0
    for (lhs, rhs) in input:
        lhs2 = utils.InclusiveInterval.from_tuple(lhs)
        rhs2 = utils.InclusiveInterval.from_tuple(rhs)
        if lhs2.overlaps(rhs2):
            result += 1
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
