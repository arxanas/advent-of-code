from __future__ import annotations

from dataclasses import dataclass

from pystreamapi import Stream

from .. import utils as u

TEST_INPUT1 = r"""
987654321111111
811111111111119
234234234234278
818181911112111
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 357
PART_2_ANSWER = 3121910778619


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    input: u.DenseGrid[str]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(input=u.DenseGrid.from_str(input))

    def part1(self, length: int = 2) -> int:
        return (
            Stream.of(self.input.rows())
            .map(lambda row: u.max_subsequence(row, length=length))
            .map(lambda seq: int("".join(seq)))
            .numeric()
            .sum()
        )

    def part2(self) -> int:
        return self.part1(length=12)
