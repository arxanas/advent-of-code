from functools import *
from itertools import *
from typing import Sequence

from .. import utils as u

Input = list[list[int]]

TEST_INPUT1 = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 114
PART_2_ANSWER = 2


def test_part1() -> None:
    assert Solution().part1(Solution().parse_input(TEST_INPUT1)) == PART_1_ANSWER


def test_part2() -> None:
    assert Solution().part2(Solution().parse_input(TEST_INPUT2)) == PART_2_ANSWER


def interpolate(seq: Sequence[int]) -> int:
    diffs = [a - b for a, b in zip(seq[1:], seq)]
    if u.all_same(diffs):
        return seq[-1] + diffs[0]
    else:
        return seq[-1] + interpolate(diffs)


class Solution(u.Solution[Input]):
    def parse_input(self, input: str) -> Input:
        result = []
        for line in input.strip().splitlines():
            result.append(u.extract_int_list(line))
        return result

    def part1(self, input: Input) -> int:
        return sum(interpolate(seq) for seq in input)

    def part2(self, input: Input) -> int:
        return sum(interpolate(list(reversed(seq))) for seq in input)
