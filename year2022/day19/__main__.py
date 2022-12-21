from __future__ import annotations

from dataclasses import dataclass
import collections
from enum import Enum
import functools
import itertools
import logging
import math
import multiprocessing
import os
import re
import sys
from typing import (
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    cast,
)
from typing_extensions import Literal

from .. import utils as u

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

    def __repr__(self) -> str:
        return f"Wallet({self._amounts})"

    def __iter__(self) -> Iterator[tuple[T, int]]:
        return iter(self._amounts.items())

    def __getitem__(self, key: T) -> int:
        return self._amounts.get(key, 0)

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
        amounts = {}
        for key in self._amounts.keys() | other._amounts.keys():
            amounts[key] = self._amounts.get(key, 0) - other._amounts.get(key, 0)
        return Wallet(amounts=amounts)

    def __mul__(self, other: int) -> "Wallet[T]":
        return Wallet(
            amounts={key: value * other for key, value in self._amounts.items()}
        )

    def __matmul__(self, other: "Wallet[T]") -> "Wallet[T]":
        return Wallet(
            amounts={key: value * other[key] for key, value in self._amounts.items()}
        )

    def __lt__(self, other: "Wallet[T]") -> bool:
        return all(
            self._amounts.get(key, 0) < other._amounts.get(key, 0)
            for key in self._amounts.keys() | other._amounts.keys()
        )

    def __le__(self, other: "Wallet[T]") -> bool:
        return all(
            self._amounts.get(key, 0) <= other._amounts.get(key, 0)
            for key in self._amounts.keys() | other._amounts.keys()
        )

    def __gt__(self, other: "Wallet[T]") -> bool:
        return all(
            self._amounts.get(key, 0) > other._amounts.get(key, 0)
            for key in self._amounts.keys() | other._amounts.keys()
        )

    def __ge__(self, other: "Wallet[T]") -> bool:
        return all(
            self._amounts.get(key, 0) >= other._amounts.get(key, 0)
            for key in self._amounts.keys() | other._amounts.keys()
        )

    def normalize(self) -> "Wallet[T]":
        return Wallet(
            amounts={key: value for key, value in self._amounts.items() if value != 0}
        )

    def __hash__(self) -> int:
        return self._hash


class ResourceWallet:
    __slots__ = ("ore", "clay", "obsidian", "geode")

    def __init__(self, ore: int = 0, clay: int = 0, obsidian: int = 0, geode: int = 0):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode

    def __repr__(self) -> str:
        return "R" + "".join(
            "/{}:{}".format(k, v)
            for (k, v) in [
                ("o", self.ore),
                ("c", self.clay),
                ("b", self.obsidian),
                ("g", self.geode),
            ]
            if v != 0
        )

    # def __lt__(self, other: ResourceWallet) -> bool:
    #     return (
    #         self.ore < other.ore
    #         and self.clay < other.clay
    #         and self.obsidian < other.obsidian
    #         and self.geode < other.geode
    #     )

    # def __le__(self, other: ResourceWallet) -> bool:
    #     return (
    #         self.ore <= other.ore
    #         and self.clay <= other.clay
    #         and self.obsidian <= other.obsidian
    #         and self.geode <= other.geode
    #     )

    # def __eq__(self, other: ResourceWallet) -> bool:
    #     return (
    #         self.ore == other.ore
    #         and self.clay == other.clay
    #         and self.obsidian == other.obsidian
    #         and self.geode == other.geode
    #     )

    # def __gt__(self, other: ResourceWallet) -> bool:
    #     return (
    #         self.ore > other.ore
    #         and self.clay > other.clay
    #         and self.obsidian > other.obsidian
    #         and self.geode > other.geode
    #     )

    # def __ge__(self, other: ResourceWallet) -> bool:
    #     return (
    #         self.ore >= other.ore
    #         and self.clay >= other.clay
    #         and self.obsidian >= other.obsidian
    #         and self.geode >= other.geode
    #     )

    def is_nonnegative(self) -> bool:
        return (
            self.ore >= 0 and self.clay >= 0 and self.obsidian >= 0 and self.geode >= 0
        )

    def add_ore(self, value: int) -> ResourceWallet:
        return ResourceWallet(
            ore=self.ore + value,
            clay=self.clay,
            obsidian=self.obsidian,
            geode=self.geode,
        )

    def add_clay(self, value: int) -> ResourceWallet:
        return ResourceWallet(
            ore=self.ore,
            clay=self.clay + value,
            obsidian=self.obsidian,
            geode=self.geode,
        )

    def add_obsidian(self, value: int) -> ResourceWallet:
        return ResourceWallet(
            ore=self.ore,
            clay=self.clay,
            obsidian=self.obsidian + value,
            geode=self.geode,
        )

    def add_geode(self, value: int) -> ResourceWallet:
        return ResourceWallet(
            ore=self.ore,
            clay=self.clay,
            obsidian=self.obsidian,
            geode=self.geode + value,
        )


Resource = Literal["ore", "clay", "obsidian", "geode"]


@dataclass(frozen=True)
class Blueprint:
    ore_cost: ResourceWallet
    clay_cost: ResourceWallet
    obsidian_cost: ResourceWallet
    geode_cost: ResourceWallet


Input = List[Blueprint]


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
                ore_cost=ResourceWallet(
                    ore=int(match.group(2)),
                ),
                clay_cost=ResourceWallet(
                    ore=int(match.group(3)),
                ),
                obsidian_cost=ResourceWallet(
                    ore=int(match.group(4)),
                    clay=int(match.group(5)),
                ),
                geode_cost=ResourceWallet(
                    ore=int(match.group(6)),
                    obsidian=int(match.group(7)),
                ),
            )
        )
    return result


class State:
    __slots__ = ("minute", "resources", "robots")

    def __init__(self, minute: int, resources: ResourceWallet, robots: ResourceWallet):
        self.minute = minute
        self.resources = resources
        self.robots = robots

    def __repr__(self) -> str:
        return f"State(minute={self.minute!r}, resources={self.resources!r}, robots={self.robots!r})"


class Resource2(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


ResourceWallet2 = Tuple[int, int, int, int]


class State2:
    __slots__ = (
        "minute",
        "num_ore",
        "num_clay",
        "num_obsidian",
        "num_geode",
        "num_ore_robots",
        "num_clay_robots",
        "num_obsidian_robots",
        "num_geode_robots",
    )

    def __init__(
        self,
        minute: int,
        num_ore: int,
        num_clay: int,
        num_obsidian: int,
        num_geode: int,
        num_ore_robots: int,
        num_clay_robots: int,
        num_obsidian_robots: int,
        num_geode_robots: int,
    ):
        self.minute = minute
        self.num_ore = num_ore
        self.num_clay = num_clay
        self.num_obsidian = num_obsidian
        self.num_geode = num_geode
        self.num_ore_robots = num_ore_robots
        self.num_clay_robots = num_clay_robots
        self.num_obsidian_robots = num_obsidian_robots
        self.num_geode_robots = num_geode_robots


def determine_max_geodes(
    blueprint: Blueprint, blueprint_num: int, total_num_minutes: int
) -> int:
    # max_ore_requirement = max(
    #     blueprint.ore_cost.ore,
    #     blueprint.clay_cost.ore,
    #     blueprint.obsidian_cost.ore,
    #     blueprint.geode_cost.ore,
    # )
    # max_clay_requirement = max(
    #     blueprint.ore_cost.clay,
    #     blueprint.clay_cost.clay,
    #     blueprint.obsidian_cost.clay,
    #     blueprint.geode_cost.clay,
    # )
    # max_obsidian_requirement = max(
    #     blueprint.ore_cost.obsidian,
    #     blueprint.clay_cost.obsidian,
    #     blueprint.obsidian_cost.obsidian,
    #     blueprint.geode_cost.obsidian,
    # )

    # initial_state = State2(
    #     minute=0,
    #     num_ore=0,
    #     num_clay=0,
    #     num_obsidian=0,
    #     num_geode=0,
    #     num_ore_robots=1,
    #     num_clay_robots=0,
    #     num_obsidian_robots=0,
    #     num_geode_robots=0,
    # )
    # stack = [initial_state]
    # best_solution = initial_state
    # while stack:
    #     current_state = stack.pop()
    #     if current_state.minute == total_num_minutes:
    #         if current_state.num_geode > best_solution.num_geode:
    #             best_solution = current_state
    #         continue

    #     if current_state.num_ore_robots < max_ore_requirement:
    #         ore_time = 1 + math.ceil(
    #             blueprint.ore_cost.ore / current_state.num_ore_robots
    #         )
    #         if (
    #             ore_time + current_state.minute < total_num_minutes
    #             and current_state.num_ore >= blueprint.ore_cost.ore
    #         ):
    #             stack.append(
    #                 State2(
    #                     minute=current_state.minute + ore_time,
    #                     num_ore=current_state.num_ore - blueprint.ore_cost.ore,
    #                     num_clay=current_state.num_clay,
    #                     num_obsidian=current_state.num_obsidian,
    #                     num_geode=current_state.num_geode,
    #                     num_ore_robots=current_state.num_ore_robots,
    #                     num_clay_robots=current_state.num_clay_robots,
    #                     num_obsidian_robots=current_state.num_obsidian_robots,
    #                     num_geode_robots=current_state.num_geode_robots,
    #                 )
    #             )

    #     if current_state.num_clay_robots < max_clay_requirement:

    # return

    max_consumption = ResourceWallet(
        ore=max(
            blueprint.ore_cost.ore,
            blueprint.clay_cost.ore,
            blueprint.obsidian_cost.ore,
            blueprint.geode_cost.ore,
        ),
        clay=max(
            blueprint.ore_cost.clay,
            blueprint.clay_cost.clay,
            blueprint.obsidian_cost.clay,
            blueprint.geode_cost.clay,
        ),
        obsidian=max(
            blueprint.obsidian_cost.obsidian,
            blueprint.clay_cost.obsidian,
            blueprint.obsidian_cost.obsidian,
            blueprint.geode_cost.obsidian,
        ),
        geode=99999,
    )

    class ShortestPath(u.BestPath):
        def __init__(self) -> None:
            super().__init__()
            self._calc_cache: dict[
                tuple[ResourceWallet, ResourceWallet, Resource],
                tuple[int, ResourceWallet],
            ] = {}

        def get_progress_key(self, path: Sequence[State]) -> Optional[str]:
            # return None
            if path:
                return "blueprint {}, geodes {}".format(
                    blueprint_num, str(path[-1].resources.geode).rjust(4, "0")
                )
            else:
                return None

        def on_new_best_path(
            self, old_path: Sequence[T], new_path: Sequence[T]
        ) -> None:
            # print("Upgraded best path from {} to {}".format(old_path, new_path))
            # if new_path[-1].resources.geode > 9:
            #     print("bad path: {!r}".format(new_path))
            pass

        def is_end_path(self, path: Sequence[State]) -> bool:
            state = path[-1]
            return state.minute == total_num_minutes + 1

        def should_prune(
            self, path: Sequence[State], best_path: Sequence[State]
        ) -> bool:
            return False
            lhs = path[-1]
            rhs = best_path[-1]
            return (
                lhs.resources.ore <= rhs.resources.ore
                and lhs.resources.clay <= rhs.resources.clay
                and lhs.resources.obsidian <= rhs.resources.obsidian
                and lhs.resources.geode <= rhs.resources.geode
                and lhs.robots.ore <= rhs.robots.ore
                and lhs.robots.clay <= rhs.robots.clay
                and lhs.robots.obsidian <= rhs.robots.obsidian
                and lhs.robots.geode <= rhs.robots.geode
                and lhs.minute > rhs.minute
            )
            #  and len(
            #     path
            # ) < len(
            #     best_path
            # )  #  and lhs != rhs

        def get_score_key(self, path: Sequence[State]) -> object:
            state = path[-1]
            remaining_minutes = total_num_minutes - state.minute
            return (
                -(state.resources.geode + (remaining_minutes * state.robots.geode)),
                -(
                    state.resources.obsidian
                    + (remaining_minutes * state.robots.obsidian)
                ),
                -(state.resources.clay + (remaining_minutes * state.robots.clay)),
                -(state.resources.ore + (remaining_minutes * state.robots.ore)),
                -remaining_minutes,
            )

        def get_heuristic_key(self, path: Sequence[State]) -> int:
            state = path[-1]
            remaining_minutes = total_num_minutes - state.minute
            return -(
                (
                    (state.resources.geode + (remaining_minutes * state.robots.geode))
                    * 10000
                )
                + (
                    (
                        state.resources.obsidian
                        + (remaining_minutes * state.robots.obsidian)
                    )
                    * 100
                )
                + (
                    (state.resources.clay + (remaining_minutes * state.robots.clay))
                    * 10
                )
                + ((state.resources.ore + (remaining_minutes * state.robots.ore)) * 100)
            )

        def calculate_time_to_construction(
            self,
            state: State,
            robot_type: Resource,
        ) -> Optional[State]:
            # print(state)
            if robot_type == "ore":
                if state.robots.ore >= max_consumption.ore:
                    return None
                cost = blueprint.ore_cost
                next_robots = ResourceWallet(
                    ore=state.robots.ore + 1,
                    clay=state.robots.clay,
                    obsidian=state.robots.obsidian,
                    geode=state.robots.geode,
                )
            elif robot_type == "clay":
                if state.robots.clay >= max_consumption.clay:
                    return None
                cost = blueprint.clay_cost
                next_robots = ResourceWallet(
                    ore=state.robots.ore,
                    clay=state.robots.clay + 1,
                    obsidian=state.robots.obsidian,
                    geode=state.robots.geode,
                )
            elif robot_type == "obsidian":
                if state.robots.obsidian >= max_consumption.obsidian:
                    return None
                cost = blueprint.obsidian_cost
                next_robots = ResourceWallet(
                    ore=state.robots.ore,
                    clay=state.robots.clay,
                    obsidian=state.robots.obsidian + 1,
                    geode=state.robots.geode,
                )
            elif robot_type == "geode":
                if state.robots.geode >= max_consumption.geode:
                    return None
                cost = blueprint.geode_cost
                next_robots = ResourceWallet(
                    ore=state.robots.ore,
                    clay=state.robots.clay,
                    obsidian=state.robots.obsidian,
                    geode=state.robots.geode + 1,
                )
            else:
                raise ValueError("Unknown robot type: {}".format(robot_type))

            # cache_key = (state.resources, state.robots, robot_type)
            # if cache_key in self._calc_cache:
            #     (time_to_construction, next_resources) = self._calc_cache[cache_key]
            #     return State(
            #         minute=state.minute + time_to_construction,
            #         resources=next_resources,
            #         robots=next_robots,
            #     )

            # We can only produce one kind of robot per unit time, so there's no
            # point in trying to increase our overall consumption.  TODO: the
            # max consumption should take the max of any robot type, instead of
            # adding consumption types.
            # if (
            #     state.robots.ore >= max_consumption.ore
            #     or state.robots.clay >= max_consumption.clay
            #     or state.robots.obsidian >= max_consumption.obsidian
            #     or state.robots.geode >= max_consumption.geode
            # ):
            #     return None

            # Check if we have enough robots to *ever* construct a new robot of
            # the given type (assuming we don't produce any other robots before
            # then).
            if (
                (cost.ore > 0 and state.robots.ore == 0)
                or (cost.clay > 0 and state.robots.clay == 0)
                or (cost.obsidian > 0 and state.robots.obsidian == 0)
                or (cost.geode > 0 and state.robots.geode == 0)
            ):
                return None

            if cost.ore > 0:
                ore_time = math.ceil(
                    (cost.ore - state.resources.ore) / state.robots.ore
                )
            else:
                ore_time = 0

            if cost.clay > 0:
                clay_time = math.ceil(
                    (cost.clay - state.resources.clay) / state.robots.clay
                )
            else:
                clay_time = 0

            if cost.obsidian > 0:
                obsidian_time = math.ceil(
                    (cost.obsidian - state.resources.obsidian) / state.robots.obsidian
                )
            else:
                obsidian_time = 0

            assert cost.geode == 0, "Nothing should consume geodes"
            geode_time = 0

            expected_time = 1 + max(
                ore_time,
                clay_time,
                obsidian_time,
                geode_time,
            )
            next_time = state.minute + expected_time
            if next_time > total_num_minutes + 1:
                return None

            next_ore = (
                state.resources.ore + (state.robots.ore * expected_time) - cost.ore
            )
            next_clay = (
                state.resources.clay + (state.robots.clay * expected_time) - cost.clay
            )
            next_obsidian = (
                state.resources.obsidian
                + (state.robots.obsidian * expected_time)
                - cost.obsidian
            )
            next_geode = (
                state.resources.geode
                + (state.robots.geode * expected_time)
                - cost.geode
            )
            assert next_geode >= state.resources.geode
            next_resources = ResourceWallet(
                ore=next_ore,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode,
            )
            assert next_resources.is_nonnegative()
            # self._calc_cache[cache_key] = (expected_time, next_resources, next_robots)
            return State(
                minute=next_time,
                resources=next_resources,
                robots=next_robots,
            )

        def get_neighbors(self, path: Sequence[State]) -> Iterable[State]:
            state = path[-1]
            # print(
            #     "minute: {!r}, resources: {!r}, robots: {!r}".format(
            #         state.minute, state.resources, state.robots
            #     )
            # )
            # if state.minute == total_num_minutes:
            # yield replace(state, minute=total_num_minutes + 1)
            # return

            if state.minute >= total_num_minutes + 1:
                return

            built_any_robot = False

            next_state = self.calculate_time_to_construction(
                state,
                "obsidian",
            )
            if next_state is not None:
                built_any_robot = True
                yield next_state

            next_state = self.calculate_time_to_construction(
                state,
                "clay",
            )
            if next_state is not None:
                built_any_robot = True
                yield next_state

            next_state = self.calculate_time_to_construction(state, "ore")
            if next_state is not None:
                built_any_robot = True
                yield next_state

            next_state = self.calculate_time_to_construction(
                state,
                "geode",
            )
            if next_state is not None:
                built_any_robot = True
                yield next_state

            if not built_any_robot:
                yield State(
                    minute=total_num_minutes + 1,
                    resources=state.resources,
                    robots=state.robots,
                )

    initial_state = State(
        minute=1,
        resources=ResourceWallet(),
        robots=ResourceWallet(ore=1),
        # total_num_geodes=0,
    )
    result = ShortestPath().find_one(initial_state, search_strategy="stack")
    # result = ShortestPath().find_one(initial_state, search_strategy="weighted-heap")
    # result = ShortestPath().find_one(initial_state, search_strategy="heap")
    # result = ShortestPath().find_one(initial_state, search_strategy="queue")
    # result = ShortestPath().find_one(initial_state, search_strategy="random")
    assert result is not None
    num_geodes = result[-1].resources.geode
    # assert num_geodes > 0
    return num_geodes
    # result = ShortestPath().find_all([initial_state])
    # return result[initial_state][-1].resources["geode"]


def job(arg: tuple[int, Blueprint]) -> int:
    (i, blueprint) = arg
    return determine_max_geodes(blueprint, i, total_num_minutes=24)


def part1(input: Input, run_in_parallel: bool) -> int:
    if run_in_parallel:
        with multiprocessing.Pool() as pool:
            max_geodes = pool.map(
                job,
                enumerate(input),
            )
    else:
        max_geodes = list(
            map(
                job,
                enumerate(input),
            )
        )

    qualities = (i * x for (i, x) in enumerate(max_geodes, 1))
    return sum(qualities)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT), run_in_parallel=False) == PART_1_ANSWER


def test_part1_input_first_blueprint() -> None:
    assert (
        part1(
            parse_input(
                """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 18 clay. Each geode robot costs 4 ore and 9 obsidian.
"""
            ),
            run_in_parallel=False,
        )
        > 0
    )


def part2(input: Input) -> int:
    result = 0
    return result


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT)) == PART_2_ANSWER


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    # 897 -- too low
    print("test 1:", part1(test_input, run_in_parallel=False))
    print("part 1:", part1(input, run_in_parallel=False))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
