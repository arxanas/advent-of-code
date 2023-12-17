from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import chain

from .. import utils as u

Input = str

TEST_INPUT1 = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 46
PART_2_ANSWER = 51


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Solution(u.Solution):
    grid: u.DenseGrid[str]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(grid=u.DenseGrid.from_str(input.strip()))

    def part1(self) -> int:
        initial_coord = u.Coord.from_2d(0, 0)
        initial_delta = u.Deltas2d.EAST
        return self._calc(initial_coord, initial_delta)

    def _calc(self, initial_coord: u.Coord, initial_delta: u.Delta) -> int:
        queue = deque[tuple[u.Coord, u.Delta]]([(initial_coord, initial_delta)])
        seen_tiles = defaultdict[u.Coord, set[u.Delta]](set)
        while queue:
            (coord, delta) = queue.popleft()
            if coord not in self.grid:
                continue
            if delta in seen_tiles[coord]:
                continue
            seen_tiles[coord].add(delta)

            match (self.grid[coord], delta):
                case (
                    (".", _)
                    | ("|", u.Deltas2d.NORTH | u.Deltas2d.SOUTH)
                    | ("-", u.Deltas2d.EAST | u.Deltas2d.WEST)
                ):
                    queue.append((coord + delta, delta))
                case ("|", u.Deltas2d.EAST | u.Deltas2d.WEST):
                    queue.append((coord + u.Deltas2d.NORTH, u.Deltas2d.NORTH))
                    queue.append((coord + u.Deltas2d.SOUTH, u.Deltas2d.SOUTH))
                case ("-", u.Deltas2d.NORTH | u.Deltas2d.SOUTH):
                    queue.append((coord + u.Deltas2d.EAST, u.Deltas2d.EAST))
                    queue.append((coord + u.Deltas2d.WEST, u.Deltas2d.WEST))
                case ("/", u.Deltas2d.EAST) | ("\\", u.Deltas2d.WEST):
                    queue.append((coord + u.Deltas2d.NORTH, u.Deltas2d.NORTH))
                case ("/", u.Deltas2d.WEST) | ("\\", u.Deltas2d.EAST):
                    queue.append((coord + u.Deltas2d.SOUTH, u.Deltas2d.SOUTH))
                case ("/", u.Deltas2d.NORTH) | ("\\", u.Deltas2d.SOUTH):
                    queue.append((coord + u.Deltas2d.EAST, u.Deltas2d.EAST))
                case ("/", u.Deltas2d.SOUTH) | ("\\", u.Deltas2d.NORTH):
                    queue.append((coord + u.Deltas2d.WEST, u.Deltas2d.WEST))
                case (cell, delta):
                    raise ValueError(f"Invalid cell {cell} with delta {delta}")
        return sum(1 for deltas in seen_tiles.values() if deltas)

    def part2(self) -> int:
        top = [(coord, u.Deltas2d.SOUTH) for (coord, _) in self.grid.iter_top_edge()]
        bottom = [
            (coord, u.Deltas2d.NORTH) for (coord, _) in self.grid.iter_bottom_edge()
        ]
        left = [(coord, u.Deltas2d.EAST) for (coord, _) in self.grid.iter_left_edge()]
        right = [(coord, u.Deltas2d.WEST) for (coord, _) in self.grid.iter_right_edge()]
        return max(
            self._calc(coord, delta)
            for (coord, delta) in chain(top, bottom, left, right)
        )
