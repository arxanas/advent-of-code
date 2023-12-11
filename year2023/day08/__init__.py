import re
from dataclasses import dataclass
from functools import *
from itertools import *
from typing import Literal

from .. import utils as u


@dataclass
class Input:
    dirs: list[Literal["L", "R"]]
    edges: dict[str, tuple[str, str]]


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
    assert Solution().part1(Solution().parse_input(TEST_INPUT1)) == PART_1_ANSWER
    assert (
        Solution().part1(
            Solution().parse_input(
                """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
            )
        )
        == 6
    )


def test_part2() -> None:
    assert Solution().part2(Solution().parse_input(TEST_INPUT2)) == PART_2_ANSWER


class Solution(u.Solution[Input]):
    def parse_input(self, input: str) -> Input:
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

        return Input(
            dirs=dirs,
            edges=edges,
        )

    def part1(self, input: Input) -> int:
        current_node = "AAA"
        count = 0
        for dir in cycle(input.dirs):
            count += 1
            (left, right) = input.edges[current_node]
            match dir:
                case "L":
                    current_node = left
                case "R":
                    current_node = right
            if current_node == "ZZZ":
                break
        return count

    def part2(self, input: Input) -> int:
        current_nodes = {node for node in input.edges.keys() if node.endswith("A")}
        count = 0
        for dir in cycle(input.dirs):
            count += 1
            next_nodes = set()
            for node in current_nodes:
                (left, right) = input.edges[node]
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
