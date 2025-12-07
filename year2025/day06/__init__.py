from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeVar

from pystreamapi import Stream

from .. import utils as u

TEST_INPUT1 = r"""
123 328  51 64_
 45 64  387 23_
  6 98  215 314
*   +   *   +__
""".replace("_", " ")

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 4277556
PART_2_ANSWER = 3263827


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True)
class Problem:
    nums: list[str]
    op: Literal["*", "+"]

    def solve(self) -> int:
        nums = [int(num.strip()) for num in self.nums]
        match self.op:
            case "*":
                return u.product_int(nums)
            case "+":
                return sum(nums)


T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    input: str

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(input=input)

    def part1(self) -> int:
        lines = u.split_lines(self.input)
        chars = u.transpose(line.split() for line in lines)
        return (
            Stream.of(chars)
            .map(lambda row: Problem(nums=row[:-1], op=row[-1]))
            .map(lambda problem: problem.solve())
            .numeric()
            .sum()
        )

    def part2(self) -> int:
        [*nums, ops] = self.input.splitlines()
        nums = u.transpose_lines(nums)
        groups = u.split_line_groups("\n".join(nums))
        return (
            Stream.of(zip(groups, ops.split()))
            .map(lambda x: Problem(nums=u.split_lines(x[0]), op=x[1]).solve())
            .numeric()
            .sum()
        )
