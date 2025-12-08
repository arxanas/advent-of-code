from __future__ import annotations

import itertools
from dataclasses import dataclass

import networkx as nx
from pystreamapi import Stream

from .. import utils as u

TEST_INPUT1 = r"""
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 40
PART_2_ANSWER = 25272


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1(num_connections=10) == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    graph: nx.Graph

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        boxes = Stream.of(u.split_lines(input)).map(
            lambda line: u.Coord(*u.extract_int_list(line))
        )
        graph = nx.Graph()
        graph.add_weighted_edges_from(
            (a, b, a.euclidean_distance(b))
            for (a, b) in itertools.combinations(boxes, 2)
        )
        return cls(graph=graph)

    def part1(self, num_connections: int = 1000) -> int:
        graph = nx.Graph()
        graph.add_weighted_edges_from(
            u.min_n(
                n=num_connections,
                iterable=self.graph.edges(data="weight"),
                key=lambda edge: edge[2],
            )
        )
        components = nx.connected_components(graph)
        max_components = u.max_n(n=3, iterable=components, key=len)
        return u.product_int(map(len, max_components))

    def part2(self) -> int:
        mst = nx.minimum_spanning_tree(self.graph)
        (a, b, _) = max(mst.edges(data=True), key=lambda edge: edge[2]["weight"])
        return a.x * b.x
