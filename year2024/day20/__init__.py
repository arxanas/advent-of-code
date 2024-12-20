from __future__ import annotations

from dataclasses import dataclass

import networkx as nx

from .. import utils as u

TEST_INPUT = r"""
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT).part1(min_saved_time=64) == 1
    assert Solution.parse_input(TEST_INPUT).part1(min_saved_time=40) == 2
    assert Solution.parse_input(TEST_INPUT).part1(min_saved_time=38) == 3
    assert Solution.parse_input(TEST_INPUT).part1(min_saved_time=36) == 4


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT).part2(min_saved_time=76) == 3
    assert Solution.parse_input(TEST_INPUT).part2(min_saved_time=74) == 3 + 4
    assert Solution.parse_input(TEST_INPUT).part2(min_saved_time=72) == 3 + 4 + 22


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    grid: u.DenseGrid[str]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(grid=u.DenseGrid.from_str(input))

    def graph(self) -> nx.Graph:
        graph = nx.Graph()
        for coord in self.grid.iter_coords():
            if self.grid[coord] == "#":
                continue
            for neighbor in self.grid.neighbors_cardinal(coord):
                if self.grid[neighbor] != "#":
                    graph.add_edge(coord, neighbor)
        return graph

    def part1(self, min_saved_time: int = 100) -> int:
        graph = self.graph()
        start_coord = u.only_exn(self.grid.find("S"))
        end_coord = u.only_exn(self.grid.find("E"))
        best_time = nx.shortest_path_length(graph, source=start_coord, target=end_coord)

        start_path_lengths = nx.single_source_shortest_path_length(
            graph, source=start_coord
        )
        end_path_lengths = nx.single_source_shortest_path_length(
            graph, source=end_coord
        )

        result = 0
        for start_node, start_length in start_path_lengths.items():
            for delta in u.Deltas2d.CARDINAL:
                cheat_neighbor = start_node + (delta * 2)
                if cheat_neighbor in end_path_lengths:
                    end_length = end_path_lengths[cheat_neighbor]
                    cheat_path_length = start_length + end_length + 2
                    if cheat_path_length <= best_time - min_saved_time:
                        result += 1
        return result

    def part2(self, min_saved_time: int = 100, max_cheat_length: int = 20) -> int:
        graph = self.graph()
        start_coord = u.only_exn(self.grid.find("S"))
        end_coord = u.only_exn(self.grid.find("E"))
        best_time = nx.shortest_path_length(graph, source=start_coord, target=end_coord)

        start_path_lengths = nx.single_source_shortest_path_length(
            graph, source=start_coord
        )
        end_path_lengths = nx.single_source_shortest_path_length(
            graph, source=end_coord
        )

        # FIXME: O(n^2), this takes a while to run:
        return sum(
            1
            for start_node, start_length in start_path_lengths.items()
            for end_node, end_length in end_path_lengths.items()
            if (cheat_length := start_node.manhattan_distance(end_node))
            <= max_cheat_length
            if start_length + cheat_length + end_length <= best_time - min_saved_time
        )
