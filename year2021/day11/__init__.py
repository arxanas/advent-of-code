import copy
import sys
from collections import *
from functools import *
from typing import *

TEST_INPUT = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

Input = List[List[int]]


def increase_charge(grid: Input) -> None:
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            grid[i][j] += 1


def do_next_flash(grid: Input) -> bool:
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if value > 9:
                grid[i][j] = -1
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        if 0 <= i + di < len(grid) and 0 <= j + dj < len(grid[0]):
                            if grid[i + di][j + dj] != -1:
                                grid[i + di][j + dj] += 1
                return True
    return False


def reset_flashed(grid: Input) -> None:
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if value == -1:
                grid[i][j] = 0


def part1(input: Input) -> str:
    input = copy.deepcopy(input)
    num_flashes = 0
    for i in range(100):
        increase_charge(input)
        while do_next_flash(input):
            num_flashes += 1
        reset_flashed(input)
    return str(num_flashes)


def part2(input: Input) -> str:
    input = copy.deepcopy(input)
    step = 0
    while True:
        step += 1
        increase_charge(input)
        while do_next_flash(input):
            pass
        if all(value == -1 for row in input for value in row):
            return str(step)
        reset_flashed(input)


def parse_input(input: str) -> Input:
    return [[int(c) for c in line] for line in input.strip().splitlines()]


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
