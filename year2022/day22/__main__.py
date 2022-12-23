from dataclasses import dataclass, replace
import collections
import functools
import itertools
import logging
import math
import os
import re
import sys
from typing import TypeVar, Union

from .. import utils as u

import z3

TEST_INPUT = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

PART_1_ANSWER = 6032
PART_2_ANSWER = 5031

Input = tuple[u.DenseGrid[str], list[Union[int, str]]]


def parse_input(input: str) -> Input:
    (map, instrs) = input.strip("\n").split("\n\n")
    lines = [line for line in map.strip("\n").splitlines()]
    max_length = max(len(x) for x in lines)
    lines = [line.ljust(max_length, " ") for line in lines]
    grid = u.DenseGrid.from_2d([list(line) for line in lines])

    instrs2: list[Union[int, str]] = []
    for match in re.finditer(r"(\d+|[RL])", instrs):
        instr = match.group(1)
        if instr.isnumeric():
            instrs2.append(int(instr))
        else:
            assert instr in ["L", "R"]
            instrs2.append(instr)
    return (grid, instrs2)


def part1(input: Input) -> int:
    (grid, instrs) = input
    start_coord = None
    for (coord, value) in grid.iter_top_edge():
        if value == ".":
            start_coord = coord
            break
    assert start_coord is not None

    pos = start_coord
    directions = [
        u.Deltas2d.EAST,
        u.Deltas2d.SOUTH,
        u.Deltas2d.WEST,
        u.Deltas2d.NORTH,
    ]
    dir_idx = 0
    for instr in instrs:
        match instr:
            case "L":
                dir_idx = (dir_idx - 1) % len(directions)
            case "R":
                dir_idx = (dir_idx + 1) % len(directions)
            case int(n):
                old_pos = pos
                for _ in range(n):
                    first = True
                    next_pos = pos
                    while first or grid[next_pos] == " ":
                        first = False
                        next_pos = next_pos + directions[dir_idx]
                        next_pos = u.Coord.from_2d(
                            next_pos.x % grid.width, next_pos.y % grid.height
                        )
                    if grid[next_pos] == "#":
                        break
                    pos = next_pos

    return (pos.y + 1) * 1000 + (pos.x + 1) * 4 + dir_idx


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


T = TypeVar("T")


def wrap_coord(grid: u.DenseGrid[T], coord: u.Coord) -> u.Coord:
    return u.Coord.from_2d(coord.x % grid.width, coord.y % grid.height)


def move_from_face(
    face_bitmap: u.DenseGrid[bool],
    coord: u.Coord,
    delta: u.Delta
    # ) -> tuple[u.Coord, u.Delta, int]:
) -> tuple[u.Coord, int]:
    stack = [coord]

    assert face_bitmap[coord]
    num_rotations = 0  # clockwise rotations
    coord = wrap_coord(face_bitmap, coord + delta)
    rotated_delta = u.Delta.from_2d(x=-1 * delta.y, y=delta.x)
    while not face_bitmap[coord]:
        coord = wrap_coord(face_bitmap, coord + rotated_delta)
        num_rotations += 1
        assert num_rotations <= 4
    # return (wrap_coord(face_bitmap, coord), delta + rotated_delta, num_rotations)
    return (wrap_coord(face_bitmap, coord), num_rotations)


def test_move_from_face() -> None:
    grid = u.DenseGrid.from_2d(
        [
            [False, False, True, False],
            [True, True, True, False],
            [False, False, True, True],
        ]
    )
    assert move_from_face(grid, coord=u.Coord.from_2d(2, 0), delta=u.Deltas2d.EAST) == (
        u.Coord.from_2d(3, 2),
        # u.Deltas2d.SOUTHEAST.d(),
        2,
    )
    assert move_from_face(grid, coord=u.Coord.from_2d(2, 1), delta=u.Deltas2d.EAST) == (
        u.Coord.from_2d(3, 2),
        # u.Deltas2d.SOUTHEAST,
        1,
    )
    assert move_from_face(
        grid, coord=u.Coord.from_2d(3, 2), delta=u.Deltas2d.NORTH
    ) == (
        u.Coord.from_2d(2, 2),
        # u.Deltas2d.WEST,
        3,
    )


def part2(input: Input) -> int:
    (grid, instrs) = input

    face_length = None
    for x in range(grid.width):
        col = ""
        for y in range(grid.height):
            col += grid[u.Coord.from_2d(x, y)]
        col = col.strip()
        if face_length is None:
            face_length = len(col)
        else:
            face_length = min(face_length, len(col))
    assert face_length is not None

    # min_row_length = None
    # for y in range(grid.height):
    #     row = ""
    #     for x in range(grid.width):
    #         row += grid[u.Coord.from_2d(x, y)]
    #     row = row.strip()
    #     if min_row_length is None:
    #         min_row_length = len(row)
    #     else:
    #         min_row_length = min(min_row_length, len(row))
    # assert min_row_length is not None

    assert grid.width % face_length == 0
    assert grid.height % face_length == 0
    face_bitmap = u.DenseGrid[bool].from_2d(
        [[False] * (grid.width // face_length)] * (grid.height // face_length)
    )
    num_faces = 0
    for x in range(0, grid.width, face_length):
        for y in range(0, grid.height, face_length):
            if grid[u.Coord.from_2d(x, y)] != " ":
                face_coord = u.Coord.from_2d(x // face_length, y // face_length)
                face_bitmap[face_coord] = True
                # face_graph[num_faces]
                num_faces += 1
    assert num_faces == 6

    start_coord = None
    for (coord, value) in grid.iter_top_edge():
        if value == ".":
            start_coord = coord
            break
    assert start_coord is not None

    pos = start_coord
    directions = [
        u.Deltas2d.EAST,
        u.Deltas2d.SOUTH,
        u.Deltas2d.WEST,
        u.Deltas2d.NORTH,
    ]
    dir_idx = 0
    for instr in instrs:
        match instr:
            case "L":
                dir_idx = (dir_idx - 1) % len(directions)
            case "R":
                dir_idx = (dir_idx + 1) % len(directions)
            case int(n):
                old_pos = pos
                for i in range(n):
                    print("Instr", i, "of", n, "at", pos, "dir", dir_idx)
                    first = True
                    next_pos = pos
                    next_dir_idx = dir_idx
                    current_face = u.Coord.from_2d(
                        pos.x // face_length, pos.y // face_length
                    )
                    while first or grid[next_pos] == " ":
                        first = False
                        if grid[next_pos] != " ":
                            next_pos = next_pos + directions[next_dir_idx]
                            next_pos = u.Coord.from_2d(
                                next_pos.x % grid.width, next_pos.y % grid.height
                            )
                        else:
                            print("  current face is", current_face)
                            (next_face, face_delta, num_rotations) = move_from_face(
                                face_bitmap, current_face, directions[next_dir_idx]
                            )
                            current_face = wrap_coord(
                                face_bitmap, current_face + face_delta
                            )
                            face_x_offset = (next_pos.x + 1) % face_length
                            face_y_offset = (next_pos.y + 1) % face_length
                            for _ in range(num_rotations):
                                face_x_offset, face_y_offset = (
                                    face_y_offset,
                                    face_length - face_x_offset,
                                )
                            next_pos = u.Coord.from_2d(
                                next_face.x * face_length + face_x_offset,
                                next_face.y * face_length + face_y_offset,
                            )
                            print("  rotated", num_rotations, "times")
                            next_dir_idx = (next_dir_idx + num_rotations) % len(
                                directions
                            )
                    if grid[next_pos] == "#":
                        break
                    pos = next_pos
                    dir_idx = next_dir_idx
                    print(f"  moved from {old_pos} to {pos} in direction {dir_idx}")
    return (pos.y + 1) * 1000 + (pos.x + 1) * 4 + dir_idx


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
