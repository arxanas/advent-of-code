from __future__ import annotations

from dataclasses import dataclass

import portion as P
from pystreamapi import Stream

from .. import utils as u

TEST_INPUT1 = r"""
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 3
PART_2_ANSWER = 14


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    fresh: list[P.Interval]
    available: list[int]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        (fresh, available) = u.split_line_groups(input)
        return cls(
            fresh=Stream.of(u.extract_int_list_pairs(fresh))
            .map(lambda x: P.closed(*x))
            .to_list(),
            available=u.extract_int_list(available),
        )

    def part1(self) -> int:
        fresh = P.Interval(*self.fresh)
        return Stream.of(self.available).filter(lambda x: x in fresh).count()

    def part2(self) -> int:
        fresh = P.Interval(*self.fresh)
        return Stream.of(fresh).map(lambda x: x.upper - x.lower + 1).numeric().sum()
