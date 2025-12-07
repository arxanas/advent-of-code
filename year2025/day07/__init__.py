from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass

from pystreamapi import Stream

from .. import utils as u

TEST_INPUT1 = r"""
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 21
PART_2_ANSWER = 40


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


def next_coords(
    grid: u.DenseGrid[str], timelines: Counter[u.Coord]
) -> Iterable[tuple[u.Coord, u.Coord]]:
    for coord in timelines.keys():
        next_coord = coord + u.Deltas2d.DOWN
        match grid.get(next_coord):
            case None:
                pass
            case ".":
                yield (coord, next_coord)
            case "^":
                for delta in [u.Deltas2d.LEFT, u.Deltas2d.RIGHT]:
                    yield (coord, next_coord + delta)
            case cell:
                raise ValueError(f"unexpected cell {cell=}")


def step(
    grid: u.DenseGrid[str], timelines: Counter[u.Coord]
) -> tuple[u.DenseGrid[str], Counter[u.Coord]]:
    next_grid = grid.copy()
    next_timelines = Counter[u.Coord]()
    for coord, next_coord in next_coords(grid=grid, timelines=timelines):
        next_grid[next_coord] = "|"
        next_timelines[next_coord] += timelines[coord]
    return next_grid, next_timelines


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    input: u.DenseGrid[str]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(input=u.DenseGrid.from_str(input))

    def simulate(self) -> tuple[u.DenseGrid[str], Counter[u.Coord]]:
        grid = self.input
        timelines = Counter[u.Coord]({grid.find_only_exn("S"): 1})
        while True:
            grid, next_timelines = step(grid=grid, timelines=timelines)
            if not next_timelines:
                break
            timelines = next_timelines
        return (grid, timelines)

    def part1(self) -> int:
        grid, _ = self.simulate()
        return (
            Stream.of(grid.find("^"))
            .filter(lambda coord: grid.get(coord + u.Deltas2d.UP) == "|")
            .count()
        )

    def part2(self) -> int:
        _, timelines = self.simulate()
        return sum(timelines.values())
