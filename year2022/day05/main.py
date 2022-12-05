import copy
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import utils

TEST_INPUT = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

PART_1_ANSWER = "CMZ"
PART_2_ANSWER = "MCD"

Input = tuple[list[list[str]], list[tuple[int, int, int]]]


def parse_input(input: str) -> Input:
    (crate_lines, step_lines) = input.strip("\n").split("\n\n")
    crate_lines2 = crate_lines.splitlines()[:-1]
    crates: list[list[str]] = [[] for i in range(len(crate_lines2))]
    for line in crate_lines2:
        for (i, c) in enumerate(line):
            if (i - 1) % 4 == 0:
                if c.isalpha():
                    crate_num = (i - 1) // 4
                    assert len(c) == 1
                    while len(crates) <= crate_num:
                        crates.append([])
                    crates[crate_num].append(c)
    for crate in crates:
        crate.reverse()

    steps = []
    for line in step_lines.splitlines():
        (_, move, _, from_, _, to) = line.split()
        move2 = int(move)
        from2 = int(from_)
        to2 = int(to)
        steps.append((move2, from2, to2))

    return (crates, steps)


def part1(input: Input) -> str:
    (crates, moves) = input
    crates = copy.deepcopy(crates)
    for (move, from_, to) in moves:
        to = to - 1
        utils.assert_in_bounds(crates, to)
        from_ = from_ - 1
        utils.assert_in_bounds(crates, from_)
        for _ in range(move):
            crates[to].append(crates[from_].pop())
    top_crates = [crate[-1] if crate else " " for crate in crates]
    return "".join(top_crates)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> str:
    (crates, moves) = input
    crates = copy.deepcopy(crates)
    for (move, from_, to) in moves:
        to = to - 1
        utils.assert_in_bounds(crates, to)
        from_ = from_ - 1
        utils.assert_in_bounds(crates, from_)
        to_move = []
        for _ in range(move):
            to_move.append(crates[from_].pop())
        to_move.reverse()
        crates[to].extend(to_move)
    top_crates = [crate[-1] if crate else " " for crate in crates]
    return "".join(top_crates)


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
