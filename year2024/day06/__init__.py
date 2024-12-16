from __future__ import annotations

from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 41
PART_2_ANSWER = 6


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Path:
    seen_cells: set[tuple[u.Coord, u.Delta]]
    did_loop: bool

    def seen_coords(self) -> set[u.Coord]:
        return set(coord for (coord, _delta) in self.seen_cells)


@dataclass
class Solution(u.Solution):
    grid: u.DenseGrid[str]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(grid=u.DenseGrid.from_str(input))

    @staticmethod
    def observe_path(grid: u.DenseGrid[str], start_coord: u.Coord) -> Path:
        seen_cells = set()
        curr_delta = u.Deltas2d.UP
        curr_coord = start_coord
        while True:
            if (curr_coord, curr_delta) in seen_cells:
                did_loop = True
                break
            seen_cells.add((curr_coord, curr_delta))
            next_coord = curr_coord + curr_delta
            if next_coord not in grid:
                did_loop = False
                break
            elif grid[next_coord] == "#":
                curr_delta = curr_delta.rotate_cw()
            else:
                curr_coord = next_coord
        return Path(seen_cells=seen_cells, did_loop=did_loop)

    def part1(self) -> int:
        start_coord = u.only_exn(self.grid.find("^"))
        path = self.observe_path(self.grid, start_coord)
        return len(path.seen_coords())

    def part2(self) -> int:
        start_coord = u.only_exn(self.grid.find("^"))
        initial_path = self.observe_path(self.grid, start_coord)
        result = 0
        for turn_coord in initial_path.seen_coords():
            path = self.observe_path(self.grid.replace({turn_coord: "#"}), start_coord)
            if path.did_loop:
                result += 1
        return result
