import itertools
import logging
import math
import re
import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple, TypeVar

from .. import utils as u

TEST_INPUT = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

PART_1_ANSWER = 1651
PART_2_ANSWER = 1707

ValveName = str


@dataclass
class ValveInfo:
    flow_rate: int
    neighbors: List[ValveName]


Input = Dict[ValveName, ValveInfo]

T = TypeVar("T")


def parse_input(input: str) -> Input:
    result = {}
    for match in re.finditer(
        r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)", input
    ):
        result[match[1]] = ValveInfo(
            flow_rate=int(match[2]), neighbors=match[3].split(", ")
        )
    return result


def score(input: Input, solution: Dict[ValveName, int], total_minutes: int) -> int:
    return sum(
        (total_minutes - minute) * input[valve].flow_rate
        for (valve, minute) in solution.items()
    )


def solve(
    input: Input,
    non_zero_valves: Set[ValveName],
    distances: Dict[Tuple[ValveName, ValveName], int],
    total_minutes: int,
) -> Tuple[int, Dict[ValveName, int]]:
    class Solution(u.BestPath):
        def get_score_key(self, path: List[Dict[ValveName, int]]) -> object:
            return -score(input, path[-1], total_minutes=total_minutes)

        def is_end_node(self, node: Dict[ValveName, int]) -> bool:
            return max(node.values()) == total_minutes

        def get_neighbors(
            self, current: Dict[ValveName, int]
        ) -> Iterable[Dict[ValveName, int]]:
            (current_valve, current_time) = max(current.items(), key=lambda x: x[1])
            neighbors = non_zero_valves - set(current.keys())
            for neighbor in neighbors:
                distance = distances.get((current_valve, neighbor))
                if distance is None:
                    continue
                new_time = current_time + distance + 1
                if new_time <= total_minutes:
                    yield {**current, neighbor: new_time}

    solution = Solution()
    best_solution = solution.find_one({"AA": 0}, search_strategy="stack")
    assert best_solution is not None
    best_path = best_solution[-1]
    best_score = score(input, best_path, total_minutes=total_minutes)
    return (best_score, best_path)

    initial_solution = {"AA": 0}
    stack: List[Dict[ValveName, int]] = [initial_solution]
    best_solution: Tuple[int, Dict[ValveName, int]] = (
        score(input, initial_solution, total_minutes),
        initial_solution,
    )
    while stack:
        current = stack.pop()
        if not current:
            current_time = 0
            current_valve = "AA"
        else:
            (current_valve, current_time) = max(current.items(), key=lambda x: x[1])
        if current_time > total_minutes:
            continue
        current_score = score(input, current, total_minutes=total_minutes)
        if current_score >= best_solution[0]:
            best_solution = (current_score, current)

        neighbors = non_zero_valves - set(current.keys())
        for neighbor in neighbors:
            distance = distances.get((current_valve, neighbor))
            if distance is None:
                continue
            new_solution = {**current, neighbor: current_time + distance + 1}
            stack.append(new_solution)
    return best_solution


def part1(input: Input) -> int:
    adjacency = {
        name: {neighbor: 1 for neighbor in info.neighbors if name != neighbor}
        for name, info in input.items()
    }
    distances = u.floyd_warshall(adjacency)
    assert any(v > 1 for v in distances.values())  # Sanity check.

    non_zero_valves = [name for (name, info) in input.items() if info.flow_rate > 0]
    (best_score, _) = solve(input, set(non_zero_valves), distances, total_minutes=30)
    return best_score


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    adjacency = {
        name: {neighbor: 1 for neighbor in info.neighbors if name != neighbor}
        for name, info in input.items()
    }
    distances = u.floyd_warshall(adjacency)

    non_zero_valves = {name for (name, info) in input.items() if info.flow_rate > 0}
    best_score = 0
    for i in range(math.ceil(len(non_zero_valves) / 2) + 1):
        for valves in itertools.combinations(non_zero_valves, i):
            lhs = set(valves)
            rhs = non_zero_valves - lhs
            lhs_score, lhs_solution = solve(
                input=input,
                non_zero_valves=lhs,
                distances=distances,
                total_minutes=26,
            )
            rhs_score, rhs_solution = solve(
                input=input,
                non_zero_valves=rhs,
                distances=distances,
                total_minutes=26,
            )
            current_score = lhs_score + rhs_score
            if current_score > best_score:
                logging.info(
                    "(part 2) Found score %d: %r %r",
                    current_score,
                    lhs_solution,
                    rhs_solution,
                )
                best_score = current_score

    return best_score


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT)) == PART_2_ANSWER


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
