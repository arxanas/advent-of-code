from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pystreamapi import Stream

from .. import utils as u

TEST_INPUT1 = r"""
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 1930
PART_2_ANSWER = 1206


def test_part1_example2() -> None:
    input = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
    assert Solution.parse_input(input).part1() == 772


def test_part2_example1() -> None:
    input = """
AAAA
BBCD
BBCC
EEEC
"""
    assert Solution.parse_input(input).part2() == 80


def test_part2_example2() -> None:
    input = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""
    assert Solution.parse_input(input).part2() == 236


def test_part2_example3() -> None:
    input = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""
    assert Solution.parse_input(input).part2() == 368


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Solution(u.Solution):
    grid: u.DenseGrid[str]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(grid=u.DenseGrid.from_str(input))

    def region_price_part1(self, region: set[u.Coord]) -> int:
        area = len(region)
        perimeter = 0
        for coord in region:
            for delta in u.Deltas2d.CARDINAL:
                if coord + delta not in region:
                    perimeter += 1
        return area * perimeter

    def region_price_part2(self, region: set[u.Coord]) -> int:
        fences: dict[u.Coord, set[u.Delta]] = {}
        for coord in region:
            for delta in u.Deltas2d.CARDINAL:
                if coord + delta not in region:
                    if coord not in fences:
                        fences[coord] = set()
                    fences[coord].add(delta)

        class SideFloodFill(u.FloodFill[tuple[u.Coord, u.Delta]]):
            def get_neighbors(
                self, node: tuple[u.Coord, u.Delta]
            ) -> Iterable[tuple[u.Coord, u.Delta]]:
                (coord, delta) = node
                for neighbor_delta in u.Deltas2d.CARDINAL:
                    neighbor_coord = coord + neighbor_delta
                    if neighbor_coord in fences and delta in fences[neighbor_coord]:
                        yield (neighbor_coord, delta)

        area = len(region)
        sides = SideFloodFill().connected_components(
            ((k, v) for k, v_set in fences.items() for v in v_set)
        )
        return area * len(sides.components)

    def part1(self) -> int:
        return (
            Stream.of(
                u.GridFloodFill(self.grid)
                .connected_components(self.grid.iter_coords())
                .components
            )
            .map(self.region_price_part1)
            .numeric()
            .sum()
        )

    def part2(self) -> int:
        return (
            Stream.of(
                u.GridFloodFill(self.grid)
                .connected_components(self.grid.iter_coords())
                .components
            )
            .map(self.region_price_part2)
            .numeric()
            .sum()
        )
