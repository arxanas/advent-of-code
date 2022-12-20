from dataclasses import dataclass, replace
import collections
import functools
import itertools
import logging
import math
import os
import re
import sys
from typing import Generic, Iterator, Literal, Optional, TypeVar

from .. import utils as u

import z3

TEST_INPUT = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""

PART_1_ANSWER = 33
PART_2_ANSWER = 0


T = TypeVar("T")


class Wallet(Generic[T]):
    def __init__(self, amounts: Optional[dict[T, int]] = None) -> None:
        if amounts is None:
            self._amounts = {}
        else:
            self._amounts = amounts
        self._hash = hash(tuple(sorted(self._amounts.items())))

    def is_nonnegative(self) -> bool:
        return all(value >= 0 for value in self._amounts.values())

    def add(self, key: T, value: int) -> "Wallet[T]":
        return Wallet(amounts={**self._amounts, key: self._amounts.get(key, 0) + value})

    def set(self, key: T, value: int) -> "Wallet[T]":
        return Wallet(amounts={**self._amounts, key: value})

    def __iter__(self) -> Iterator[tuple[T, int]]:
        return iter(self._amounts.items())

    def __getitem__(self, key: T) -> int:
        return self._amounts[key]

    def __setitem__(self, key: T, value: int) -> None:
        self._amounts[key] = value

    def __contains__(self, key: T) -> bool:
        return self._amounts.get(key, 0) > 0

    def __add__(self, other: "Wallet[T]") -> "Wallet[T]":
        return Wallet(
            amounts=collections.Counter(self._amounts)
            + collections.Counter(other._amounts)
        )

    def __sub__(self, other: "Wallet[T]") -> "Wallet[T]":
        return Wallet(
            amounts=collections.Counter(self._amounts)
            - collections.Counter(other._amounts)
        )

    def __lt__(self, other: "Wallet[T]") -> bool:
        return all(
            self._amounts.get(key, 0) < other._amounts.get(key, 0)
            for key in set(self._amounts) | set(other._amounts)
        )

    def __le__(self, other: "Wallet[T]") -> bool:
        return all(
            self._amounts.get(key, 0) <= other._amounts.get(key, 0)
            for key in set(self._amounts) | set(other._amounts)
        )

    def __gt__(self, other: "Wallet[T]") -> bool:
        return all(
            self._amounts.get(key, 0) > other._amounts.get(key, 0)
            for key in set(self._amounts) | set(other._amounts)
        )

    def __ge__(self, other: "Wallet[T]") -> bool:
        return all(
            self._amounts.get(key, 0) >= other._amounts.get(key, 0)
            for key in set(self._amounts) | set(other._amounts)
        )

    def normalize(self) -> "Wallet[T]":
        return Wallet(
            amounts={key: value for key, value in self._amounts.items() if value != 0}
        )

    def __hash__(self) -> int:
        return self._hash


Resource = Literal["ore", "clay", "obsidian", "geode"]


@dataclass(frozen=True)
class Blueprint:
    costs: dict[Resource, Wallet[Resource]]


Input = list[Blueprint]


def parse_input(input: str) -> Input:
    result = []
    for line in input.strip().splitlines():
        match = re.match(
            r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.",
            line,
        )
        assert match is not None
        result.append(
            Blueprint(
                costs={
                    "ore": Wallet(
                        amounts={
                            "ore": int(match.group(2)),
                        }
                    ),
                    "clay": Wallet(amounts={"ore": int(match.group(3))}),
                    "obsidian": Wallet(
                        amounts={
                            "ore": int(match.group(4)),
                            "clay": int(match.group(5)),
                        }
                    ),
                    "geode": Wallet(
                        amounts={
                            "ore": int(match.group(6)),
                            "obsidian": int(match.group(7)),
                        }
                    ),
                }
            )
        )
    return result


@dataclass(frozen=True)
class State:
    minute: int
    resources: Wallet[Resource]
    robots: Wallet[Resource]


def determine_max_geodes(blueprint: Blueprint, total_num_minutes: int) -> int:
    class ShortestPath(u.BestPath):
        def __init__(self) -> None:
            super().__init__()
            self._minute = 0

        def get_progress_key(self, state: State) -> Optional[str]:
            return "minute " + str(state.minute).rjust(2, "0")

        def get_score_key(self, lhs: list[State], rhs: list[State]) -> bool:
            def extrapolate_geodes(state: State) -> int:
                return state.resources["geode"] + (
                    (total_num_minutes - state.minute) * state.robots["geode"]
                )

            return extrapolate_geodes(lhs[-1]) > extrapolate_geodes(rhs[-1])

        def get_neighbors(self, state: State) -> list[State]:
            state = replace(
                state,
                minute=state.minute + 1,
                resources=state.resources + state.robots,
            )

            next_states = []
            for robot_type, cost in blueprint.costs.items():
                next_resources = state.resources - cost
                if next_resources.is_nonnegative():
                    next_states.append(
                        replace(
                            state,
                            resources=next_resources,
                            robots=state.robots.add(robot_type, 1),
                        )
                    )

            return next_states

        def is_end_node(self, state: State) -> bool:
            return state.minute == total_num_minutes

    initial_state = State(
        minute=0,
        resources=Wallet(),
        robots=Wallet(
            amounts={
                "ore": 1,
            }
        ),
    )
    result: dict[State, list[State]] = ShortestPath().find_all([initial_state])
    return result[initial_state][-1].resources["geode"]


def part1(input: Input) -> int:
    max_geodes = [
        determine_max_geodes(blueprint, total_num_minutes=24) for blueprint in input
    ]
    qualities = [i * x for (i, x) in enumerate(max_geodes)]
    return sum(qualities)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    result = 0
    return result


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT)) == PART_2_ANSWER


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
