from __future__ import annotations

import re
from dataclasses import dataclass

from pystreamapi import Stream

from .. import utils as u

TEST_INPUT1 = r"""
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 1227775554
PART_2_ANSWER = 4174379265


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    input: list[tuple[int, int]]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(input=u.extract_int_list_pairs(input))

    def part1(self) -> int:
        return (
            Stream.of(self.input)
            .flat_map(lambda pair: Stream.of(range(pair[0], pair[1] + 1)))
            .filter(lambda num: re.match(r"^(\d+?)\1$", str(num)))
            .numeric()
            .sum()
        )

    def part2(self) -> int:
        return (
            Stream.of(self.input)
            .flat_map(lambda pair: Stream.of(range(pair[0], pair[1] + 1)))
            .filter(lambda num: re.match(r"^(\d+?)\1+$", str(num)))
            .numeric()
            .sum()
        )
