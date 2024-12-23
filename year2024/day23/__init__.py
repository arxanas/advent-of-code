from __future__ import annotations

from dataclasses import dataclass

import networkx as nx

from .. import utils as u

TEST_INPUT1 = r"""
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 7
PART_2_ANSWER = "co,de,ka,ta"


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    edges: list[tuple[str, str]]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(edges=[u.tuple2(line.split("-")) for line in u.split_lines(input)])

    def part1(self) -> int:
        graph = nx.Graph()
        for lhs, rhs in self.edges:
            graph.add_edge(lhs, rhs)

        cliques = [
            clique
            for clique in nx.enumerate_all_cliques(graph)
            if len(clique) == 3
            if any(node.startswith("t") for node in clique)
        ]
        return len(cliques)

    def part2(self) -> str:
        graph = nx.Graph()
        for lhs, rhs in self.edges:
            graph.add_node(lhs, weight=1)
            graph.add_node(rhs, weight=1)
            graph.add_edge(lhs, rhs)
        (c, _cost) = nx.max_weight_clique(graph)
        return ",".join(sorted(c))
