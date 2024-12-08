from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import *
from itertools import *
from typing import Self

import pytest

from .. import utils as u

TEST_INPUT11 = """
.....
.S-7.
.|.|.
.L-J.
.....
"""
TEST_INPUT12 = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

TEST_INPUT21 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""
TEST_INPUT22 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""
TEST_INPUT23 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT11).part1() == 4
    assert Solution.parse_input(TEST_INPUT12).part1() == 8


@pytest.mark.xfail
def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT21).part2() == 4
    assert Solution.parse_input(TEST_INPUT22).part2() == 8
    assert Solution.parse_input(TEST_INPUT23).part2() == 10


@dataclass
class Solution(u.Solution):
    grid: u.DenseGrid[str]

    @classmethod
    def parse_input(cls, input: str) -> Self:
        chars = [list(line) for line in input.strip().splitlines()]
        return cls(u.DenseGrid.from_2d(chars))

    def part1(self) -> int:
        def direction(c: str) -> list[u.Delta]:
            match c:
                case "|":
                    deltas = [u.Deltas2d.NORTH, u.Deltas2d.SOUTH]
                case "-":
                    deltas = [u.Deltas2d.EAST, u.Deltas2d.WEST]
                case "L":
                    deltas = [u.Deltas2d.NORTH, u.Deltas2d.EAST]
                case "J":
                    deltas = [u.Deltas2d.NORTH, u.Deltas2d.WEST]
                case "7":
                    deltas = [u.Deltas2d.SOUTH, u.Deltas2d.WEST]
                case "F":
                    deltas = [u.Deltas2d.SOUTH, u.Deltas2d.EAST]
                case ".":
                    deltas = []
            return deltas

        start_coord = next(coord for coord, c in self.grid.iter_cells() if c == "S")
        start_deltas = []
        for (
            start_neighbor,
            start_neighbor_cell,
            start_neighbor_delta,
        ) in self.grid.iter_deltas(start_coord, u.Deltas2d.CARDINAL, max_steps=1):
            if start_neighbor_delta.invert() in direction(start_neighbor_cell):
                start_deltas.append(start_neighbor_delta)
        assert len(start_deltas) == 2

        # TODO: extract into Dijkstra's algorithm
        # TODO: explain what Floyd-Warshall's does and how it differs
        best_paths: dict[u.Coord, int] = {}
        next_coords = deque([(start_coord, 0)])
        while next_coords:
            coord, distance = next_coords.popleft()
            if coord not in self.grid:
                continue
            if coord in best_paths and best_paths[coord] <= distance:
                continue
            best_paths[coord] = distance
            match self.grid[coord]:
                case "S":
                    deltas = start_deltas
                case "|":
                    deltas = [u.Deltas2d.NORTH, u.Deltas2d.SOUTH]
                case "-":
                    deltas = [u.Deltas2d.EAST, u.Deltas2d.WEST]
                case "L":
                    deltas = [u.Deltas2d.NORTH, u.Deltas2d.EAST]
                case "J":
                    deltas = [u.Deltas2d.NORTH, u.Deltas2d.WEST]
                case "7":
                    deltas = [u.Deltas2d.SOUTH, u.Deltas2d.WEST]
                case "F":
                    deltas = [u.Deltas2d.SOUTH, u.Deltas2d.EAST]
                case ".":
                    continue
            next_coords.extend((coord + delta, distance + 1) for delta in deltas)
        return max(best_paths.values())

    def part2(self) -> int:
        result = 0
        return result
