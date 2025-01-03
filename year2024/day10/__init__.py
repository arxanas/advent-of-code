from __future__ import annotations

from dataclasses import dataclass

from pystreamapi import Stream

from .. import utils as u

TEST_INPUT1 = r"""
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 36
PART_2_ANSWER = 81


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    grid: u.DenseGrid[int]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(grid=u.DenseGrid.from_str_mapped(input.strip(), int))

    def part1(self) -> int:
        class FloodFill(u.GridFloodFill):
            grid: u.DenseGrid[int]

            def are_connected(self, node: u.Coord, neighbor: u.Coord) -> bool:
                return self.grid[neighbor] == self.grid[node] + 1

        flood_fill = FloodFill(grid=self.grid)
        return (
            Stream.of(self.grid.find(0))
            .map(lambda coord: flood_fill.run([coord]))
            .flat_map(Stream.of)
            .filter(lambda coord: self.grid[coord] == 9)
            .count()
        )

    def part2(self) -> int:
        def num_paths(start_node: u.Coord) -> int:
            if self.grid[start_node] == 9:
                return 1

            return (
                Stream.of(self.grid.neighbors_cardinal(start_node))
                .filter(
                    lambda neighbor: self.grid[neighbor] == self.grid[start_node] + 1
                )
                .map(num_paths)
                .numeric()
                .sum()
            )

        return Stream.of(self.grid.find(0)).map(num_paths).numeric().sum()
