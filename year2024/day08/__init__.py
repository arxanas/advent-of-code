from __future__ import annotations

import itertools
from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 14
PART_2_ANSWER = 34


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


def test_part2_example() -> None:
    assert (
        Solution.parse_input(
            """
T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........
""",
        ).part2()
        == 9
    )


@dataclass
class Solution(u.Solution):
    grid: u.DenseGrid[str]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(grid=u.DenseGrid.from_str(input))

    def part1(self) -> int:
        nodes = u.group_by(
            (cell, coord)
            for (coord, cell) in self.grid.find_where(lambda cell: cell != ".")
        )
        antinode_coords = set()
        for node_coords in nodes.values():
            for lhs, rhs in itertools.combinations(node_coords, 2):
                antinode_coords.add(lhs + (lhs - rhs))
                antinode_coords.add(rhs + (rhs - lhs))
        return u.count(coord for coord in antinode_coords if coord in self.grid)

    def part2(self) -> int:
        nodes = u.group_by(
            (cell, coord)
            for (coord, cell) in self.grid.find_where(lambda cell: cell != ".")
        )
        antinode_coords = set()

        def iter_delta(coord: u.Coord, delta: u.Delta) -> None:
            while coord in self.grid:
                antinode_coords.add(coord)
                coord += delta

        for node_coords in nodes.values():
            for lhs, rhs in itertools.combinations(node_coords, 2):
                iter_delta(coord=rhs, delta=lhs - rhs)
                iter_delta(coord=lhs, delta=rhs - lhs)
        return len(antinode_coords)
