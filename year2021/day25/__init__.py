from __future__ import annotations

import copy
import sys
from typing import List

TEST_INPUT = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""

Grid = List[List[str]]


def parse_input(input: str) -> Grid:
    return [list(s) for s in input.strip().splitlines()]


def step_east(grid: Grid) -> Grid:
    new_grid = copy.deepcopy(grid)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            n = (j + 1) % len(row)
            if c == ">" and grid[i][n] == ".":
                new_grid[i][j] = "."
                new_grid[i][n] = ">"
    return new_grid


def step_south(grid: Grid) -> Grid:
    new_grid = copy.deepcopy(grid)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            n = (i + 1) % len(grid)
            if c == "v" and grid[n][j] == ".":
                new_grid[i][j] = "."
                new_grid[n][j] = "v"
    return new_grid


def print_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))


def main() -> None:
    # grid = parse_input(TEST_INPUT)
    input = sys.stdin.read()
    grid = parse_input(input)
    i = 0
    while True:
        i += 1
        next_grid = step_east(grid)
        next_grid = step_south(next_grid)
        if next_grid == grid:
            break
        grid = next_grid
    print(i)


if __name__ == "__main__":
    main()
