from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pystreamapi import Stream

from .. import utils as u

TEST_INPUT1 = r"""
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 3
PART_2_ANSWER = 6


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True, kw_only=True)
class State:
    dial: int

    def rotate(self, rotation: Literal["L", "R"], steps: int) -> tuple[State, int]:
        assert steps != 0
        dial = self.dial

        zeroes = 0
        for i in range(steps):
            match rotation:
                case "L":
                    dial -= 1
                case "R":
                    dial += 1
            dial %= 100
            if dial == 0:
                zeroes += 1
        return State(dial=dial), zeroes


def test_rotate() -> None:
    assert State(dial=50).rotate("R", 1000) == (State(dial=50), 10)
    assert State(dial=50).rotate("L", 100) == (State(dial=50), 1)
    assert State(dial=50).rotate("L", 50) == (State(dial=0), 1)


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    input: list[tuple[Literal["L", "R"], int]]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(
            input=Stream.of(u.split_lines(input))
            .map(lambda line: (line[0], int(line[1:])))
            .to_list()
        )

    def part1(self) -> int:
        result = 0
        state = State(dial=50)
        for rotation, steps in self.input:
            state, _ = state.rotate(rotation, steps)
            if state.dial == 0:
                result += 1
        return result

    def part2(self) -> int:
        result = 0
        state = State(dial=50)
        for rotation, steps in self.input:
            state, zeroes = state.rotate(rotation, steps)
            result += zeroes
        return result
