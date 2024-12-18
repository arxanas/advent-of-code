from __future__ import annotations

import bisect
from collections.abc import Iterable
from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 22
PART_2_ANSWER = "6,1"


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1(num_bytes=12) == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    coords: list[u.Coord]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(
            coords=[u.Coord.from_2d(x, y) for (x, y) in u.extract_int_list_pairs(input)]
        )

    def part1(self, num_bytes: int = 1024) -> int | None:
        start_coord = u.Coord.from_2d(0, 0)
        end_coord = u.Coord.from_2d(
            x=max(coord.x for coord in self.coords),
            y=max(coord.y for coord in self.coords),
        )
        corrupted_coords = set(self.coords[:num_bytes])

        class FindShortestPath(u.FindShortestPath[u.Coord]):
            def is_end_node(self, coord: u.Coord) -> bool:
                return coord == end_coord

            def get_neighbors(self, coord: u.Coord) -> Iterable[tuple[u.Coord, int]]:
                for delta in u.Deltas2d.CARDINAL:
                    new_coord = coord + delta
                    if (
                        0 <= new_coord.x <= end_coord.x
                        and 0 <= new_coord.y <= end_coord.y
                    ) and (new_coord not in corrupted_coords):
                        yield (new_coord, 1)

        result = FindShortestPath().run(start_nodes=[start_coord])
        if result:
            return result[0].cost
        else:
            return None

    def part2(self) -> str:
        num_bytes = bisect.bisect_right(
            range(len(self.coords)),
            x=False,
            key=lambda num_bytes: self.part1(num_bytes=num_bytes) is None,
        )
        bad_coord = self.coords[num_bytes - 1]
        return f"{bad_coord.x},{bad_coord.y}"
