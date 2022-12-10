import sys
from collections import deque

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
#######.......#######.......#######.....
"""

Input = list[list[str]]


def parse_input(input: str) -> Input:
    result = []
    for line in input.strip().splitlines():
        result.append(line.split())
    return result


def part1(input: Input) -> int:
    x_reg = 1
    result = 0
    clock_cycle = 0
    instrs = deque(input)
    while instrs:
        clock_cycle += 1
        if clock_cycle in [20, 60, 100, 140, 180, 220]:
            result += x_reg * clock_cycle

        instr = instrs.popleft()
        match instr:
            case ["addx", x]:
                instrs.appendleft(["add", x])
            case ["add", x]:
                x_reg += int(x)
            case ["noop"]:
                pass
            case instr:
                raise ValueError("Bad instruction: {instr!r}")
    return result


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> str:
    x_reg = 1
    result = "\n"
    clock_cycle = 0
    crt_width = 40
    instrs = deque(input)
    while instrs:
        crt_position = clock_cycle % crt_width
        if x_reg - 1 <= crt_position <= x_reg + 1:
            result += "#"
        else:
            result += "."

        clock_cycle += 1
        if clock_cycle % crt_width == 0:
            result += "\n"

        instr = instrs.popleft()
        match instr:
            case ["addx", x]:
                instrs.appendleft(["add", x])
            case ["add", x]:
                x_reg += int(x)
            case ["noop"]:
                pass
            case instr:
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
