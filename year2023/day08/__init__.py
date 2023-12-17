import re
from dataclasses import dataclass
from functools import *
from itertools import *
from typing import Literal, Self

from .. import utils as u

TEST_INPUT1 = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

TEST_INPUT2 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

PART_1_ANSWER = 2
PART_2_ANSWER = 6


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER
    assert (
        Solution.parse_input(
            """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
        ).part1()
        == 6
    )


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Solution(u.Solution):
    dirs: list[Literal["L", "R"]]
    edges: dict[str, tuple[str, str]]

    @classmethod
    def parse_input(cls, input: str) -> Self:
        (header, edge_lines) = u.split_line_groups(input.strip())
        dirs = []
        for c in header:
            match c:
                case "L" | "R":
                    dirs.append(c)
                case _:
                    raise ValueError(f"Invalid char: {c}")

        EDGE_RE = re.compile(r"(\w+) = \((\w+), (\w+)\)")
        edges = {}
        for line in edge_lines.splitlines():
            match = EDGE_RE.match(line)
            if not match:
                raise ValueError(f"Invalid edge: {line}")
            edges[match.group(1)] = (match.group(2), match.group(3))

        return cls(
            dirs=dirs,
            edges=edges,
        )

    def part1(self) -> int:
        current_node = "AAA"
        count = 0
        for dir in cycle(self.dirs):
            count += 1
            (left, right) = self.edges[current_node]
            match dir:
                case "L":
                    current_node = left
                case "R":
                    current_node = right
            if current_node == "ZZZ":
                break
        return count

    def part2(self) -> int:
        current_nodes = {node for node in self.edges.keys() if node.endswith("A")}
        count = 0
        for dir in cycle(self.dirs):
            count += 1
            next_nodes = set()
            for node in current_nodes:
                (left, right) = self.edges[node]
                match dir:
                    case "L":
                        next_node = left
                    case "R":
                        next_node = right
                next_nodes.add(next_node)
            current_nodes = next_nodes
            if all(node.endswith("Z") for node in current_nodes):
                break
        return count
