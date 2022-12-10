from collections import defaultdict
import os
import sys

from .. import utils

TEST_INPUT = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

PART_1_ANSWER = 13140
PART_2_ANSWER = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""

Input = list[list[str]]


def parse_input(input: str) -> Input:
    result = []
    for line in input.strip().splitlines():
        result.append(line.split())
    return result


def part1(input: Input) -> int:
    acc = 1
    result = 0
    i = 0
    for instr in input:
        i += 1
        if i in [20, 60, 100, 140, 180, 220]:
            result += acc * i

        if instr[0] == "addx":
            i += 1
            if i in [20, 60, 100, 140, 180, 220]:
                result += acc * i
            acc += int(instr[1])
        elif instr[0] == "noop":
            pass
        else:
            raise ValueError("Bad instruction: {instr!r}")
    return result


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> str:
    acc = 1
    result = "\n"
    width = 40

    i = 0
    for instr in input:
        i += 1
        if (acc - 1) % width <= (i - 1) % width <= (acc + 1) % width:
            result += "#"
        else:
            result += "."
        if i > 1 and (i - 1) % width == 0:
            result += "\n"

        if instr[0] == "addx":
            i += 1
            if (acc - 1) % width <= (i - 1) % width <= (acc + 1) % width:
                result += "#"
            else:
                result += "."
            if i > 1 and (i - 1) % width == 0:
                result += "\n"
            acc += int(instr[1])
        elif instr[0] == "noop":
            pass
        else:
            raise ValueError("Bad instruction: {instr!r}")
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
