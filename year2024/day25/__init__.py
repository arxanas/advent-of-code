from __future__ import annotations

import collections
import itertools
from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 3
PART_2_ANSWER = 0


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    schematics: list[u.DenseGrid[str]]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(
            schematics=[
                u.DenseGrid.from_str(group) for group in u.split_line_groups(input)
            ]
        )

    def part1(self) -> int:
        locks: list[collections.Counter[int]] = []
        keys: list[collections.Counter[int]] = []
        for schematic in self.schematics:
            heights = collections.Counter(
                coord.x for (coord, cell) in schematic.iter_cells() if cell == "#"
            )
            if schematic[u.Coord(0, 0)] == "#":
                locks.append(heights)
            else:
                keys.append(heights)

        max_height = self.schematics[0].height
        return sum(
            int(all(lock[i] + key[i] <= max_height for i in lock))
            for lock, key in itertools.product(locks, keys)
        )

    def part2(self) -> int:
        result = 0
        return result
