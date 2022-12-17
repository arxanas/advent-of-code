from dataclasses import dataclass, replace
import collections
import math
import os
import re
import sys

from .. import utils as u

import z3

TEST_INPUT = """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""

PART_1_ANSWER = 3068
PART_2_ANSWER = 1_514_285_714_288

Input = str


SHAPES = [
    # ****
    [
        u.Delta.from_2d(0, 0),
        u.Delta.from_2d(1, 0),
        u.Delta.from_2d(2, 0),
        u.Delta.from_2d(3, 0),
    ],
    # .*.
    # ***
    # .*.
    [
        u.Delta.from_2d(1, 0),
        u.Delta.from_2d(0, 1),
        u.Delta.from_2d(1, 1),
        u.Delta.from_2d(2, 1),
        u.Delta.from_2d(1, 2),
    ],
    # ..*
    # ..*
    # ***
    [
        # (upside-down due to our y-coordinates being inverted)
        u.Delta.from_2d(0, 0),
        u.Delta.from_2d(1, 0),
        u.Delta.from_2d(2, 0),
        u.Delta.from_2d(2, 1),
        u.Delta.from_2d(2, 2),
    ],
    # *
    # *
    # *
    # *
    [
        u.Delta.from_2d(0, 0),
        u.Delta.from_2d(0, 1),
        u.Delta.from_2d(0, 2),
        u.Delta.from_2d(0, 3),
    ],
    # **
    # **
    [
        u.Delta.from_2d(0, 0),
        u.Delta.from_2d(0, 1),
        u.Delta.from_2d(1, 0),
        u.Delta.from_2d(1, 1),
    ],
]


def parse_input(input: str) -> Input:
    return input.strip()


def collides(grid: set[u.Coord], shape: list[u.Coord], floor_y: int) -> bool:
    return any(
        coord.y < 0 or coord.x < 0 or coord.x >= 7 or coord in grid for coord in shape
    )


def print_grid(grid: set[u.Coord]) -> None:
    max_y = max(coord.y for coord in grid)
    min_y = min(coord.y for coord in grid)
    for y in range(max_y, min_y - 1, -1):
        for x in range(7):
            print("#" if u.Coord.from_2d(x, y) in grid else ".", end="")
        print()


def solve(input: Input, max_num_rocks: int) -> int:
    grid: set[u.Coord] = set()
    seen_states: set[tuple[int, int, frozenset[u.Coord]]] = set()
    i = 0
    num_rocks = 0
    current_shape_idx = 0
    current_shape_topleft = u.Coord.from_2d(2, 3)
    floor_y = 0
    while num_rocks < max_num_rocks:
        direction = input[i % len(input)]
        i += 1
        if direction == "<":
            direction_delta = u.Deltas2d.WEST
        elif direction == ">":
            direction_delta = u.Deltas2d.EAST
        else:
            raise ValueError("Bad direction: " + direction)

        current_shape = [
            current_shape_topleft + shape_delta
            for shape_delta in SHAPES[current_shape_idx % len(SHAPES)]
        ]
        jet_shape = [coord + direction_delta for coord in current_shape]
        if not collides(grid, jet_shape, floor_y=floor_y):
            current_shape_topleft += direction_delta
            current_shape = jet_shape

        fall_delta = u.Delta.from_2d(0, -1)
        fall_shape = [coord + fall_delta for coord in current_shape]
        if not collides(grid, fall_shape, floor_y=floor_y):
            current_shape_topleft += fall_delta
            # current_shape = fall_shape
        else:
            num_rocks += 1
            grid.update(current_shape)
            current_shape_idx += 1
            max_y = max(coord.y for coord in grid) + 1
            current_shape_topleft = u.Coord.from_2d(2, max_y + 3)

            # TODO
            # seen_xs = set()
            # grid_coords = sorted(grid, key=lambda coord: coord.y, reverse=True)
            # for coord in grid_coords:
            #     seen_xs.add(coord.x)
            #     if len(seen_xs) == 7:
            #         grid = {c for c in grid if c.y >= coord.y}
            #         print("grid", seen_xs)
            #         print_grid(grid)
            #         break

            # new_grid = set()
            # for x in range(7):
            #     x_coords = [coord for coord in grid if coord.x == x]
            #     if x_coords:
            #         max_y_coord = max(x_coords, key=lambda coord: coord.y)
            #         new_grid.add(max_y_coord)
            # grid = new_grid
            # grid = {coord for coord in grid if coord.y >= max_y - 15}
            # for y in range(max_y - 10, max_y + 1):
            #     occupied_xs = {coord for coord in grid if coord.y == y}
            #     if len(occupied_xs) == 7:
            #         print("found full row", y)
            #         # print_grid(grid)
            #         grid = {coord for coord in grid if coord.y >= y}
            #         floor_y = y - 1
            #         break
            # state = (direction, current_shape_idx, frozenset(grid))
            # state = frozenset(grid)
            # if state in seen_states:
            #     print("Saw state again!", state)
            # seen_states.add(state)
    return max(coord.y for coord in grid) + 1


def part1(input: Input, max_num_rocks: int = 2022) -> int:
    return solve(input, max_num_rocks=max_num_rocks)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    return 0
    return part1(input, max_num_rocks=1_000_000_000_000)


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
