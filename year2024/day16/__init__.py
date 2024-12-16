from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import TypeAlias, override

from .. import utils as u

TEST_INPUT1 = r"""
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 7036
PART_2_ANSWER = 45


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part1_example2() -> None:
    assert (
        Solution.parse_input("""
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""").part1()
    ) == 11048


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


def test_part2_example2() -> None:
    assert (
        Solution.parse_input("""
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""").part2()
        == 64
    )


Node: TypeAlias = tuple[u.Coord, u.Delta]


@dataclass
class FindShortestPath(u.FindShortestPath[Node]):
    grid: u.DenseGrid[str]

    @override
    def is_end_node(self, node):
        (coord, _delta) = node
        return self.grid[coord] == "E"

    @override
    def get_neighbors(self, node: Node) -> Iterable[tuple[Node, int]]:
        (coord, delta) = node
        if coord + delta in self.grid and self.grid[coord + delta] != "#":
            yield ((coord + delta, delta), 1)
        yield ((coord, delta.rotate_cw()), 1000)
        yield ((coord, delta.rotate_ccw()), 1000)


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    grid: u.DenseGrid[str]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(grid=u.DenseGrid.from_str(input.strip()))

    def find_shortest_path_nodes(self) -> list[u.ShortestPathNode[Node]]:
        start_node = (u.only_exn(self.grid.find("S")), u.Deltas2d.EAST)
        return FindShortestPath(grid=self.grid).run([start_node])

    def part1(self) -> int:
        return self.find_shortest_path_nodes()[0].cost

    def part2(self) -> int:
        return len(
            set(
                coord
                for shortest_path_node in self.find_shortest_path_nodes()
                for path in shortest_path_node.paths()
                for (coord, _delta) in path
            )
        )
