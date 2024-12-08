from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
3   4
4   3
2   5
1   3
3   9
3   3
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 11
PART_2_ANSWER = 31


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Solution(u.Solution):
    left: list[int]
    right: list[int]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        (left, right) = u.transpose(u.extract_int_list_pairs(input))
        return cls(left=left, right=right)

    def part1(self) -> int:
        return sum(
            abs(rhs - lhs) for lhs, rhs in zip(sorted(self.left), sorted(self.right))
        )

    def part2(self) -> int:
        counts = Counter(self.right)
        return sum(i * counts[i] for i in self.left)
