from __future__ import annotations

from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 2
PART_2_ANSWER = 4


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Solution(u.Solution):
    input: list[list[int]]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(input=[u.extract_int_list(line) for line in u.split_lines(input)])

    @staticmethod
    def is_safe(line: list[int]) -> bool:
        diffs = [rhs - lhs for lhs, rhs in u.sliding_windows(line, size=2)]
        signs = [diff >= 0 for diff in diffs]
        return u.all_same(signs) and all(1 <= abs(diff) <= 3 for diff in diffs)

    def part1(self) -> int:
        return u.count(line for line in self.input if self.is_safe(line))

    def part2(self) -> int:
        def remove_idx(l: list[int], idx: int) -> list[int]:
            return l[:idx] + l[idx + 1 :]

        return u.count(
            line
            for line in self.input
            if any(self.is_safe(remove_idx(line, i)) for i in range(len(line)))
        )
