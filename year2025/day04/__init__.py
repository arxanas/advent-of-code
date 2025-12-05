from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from pystreamapi import Stream

from .. import utils as u

TEST_INPUT1 = r"""
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 13
PART_2_ANSWER = 43


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    input: u.DenseGrid[str]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(input=u.DenseGrid.from_str(input))

    def removable(self, grid: u.DenseGrid[str]) -> Sequence[u.Coord]:
        return list(
            Stream.of(grid.iter_cells())
            .filter(lambda x: x[1] == "@")
            .map(lambda x: x[0])
            .filter(
                lambda coord: Stream.of(grid.neighbors(coord, u.Deltas2d.ALL))
                .filter(lambda y: grid[y] == "@")
                .count()
                < 4
            )
        )

    def part1(self) -> int:
        return len(self.removable(self.input))

    def part2(self) -> int:
        result = 0
        input = self.input.copy()
        while True:
            to_remove = self.removable(input)
            if not to_remove:
                break
            result += len(to_remove)
            input.update({coord: "." for coord in to_remove})
        return result
