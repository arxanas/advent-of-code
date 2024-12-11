from __future__ import annotations

from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
125 17
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 55312
PART_2_ANSWER = 65601038650482


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Solution(u.Solution):
    nums: list[int]
    cache: dict[tuple[int, int], int]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(nums=u.extract_int_list(input), cache={})

    def solve(self, num: int, steps: int) -> int:
        if steps == 0:
            return 1

        cache_key = (num, steps)
        if cache_key in self.cache:
            return self.cache[cache_key]

        if num == 0:
            result = self.solve(num=1, steps=steps - 1)
        elif len(val_str := str(num)) % 2 == 0:
            midpoint = len(val_str) // 2
            lhs = int(val_str[:midpoint])
            rhs = int(val_str[midpoint:])
            result = self.solve(num=lhs, steps=steps - 1) + self.solve(
                num=rhs, steps=steps - 1
            )
        else:
            result = self.solve(num=num * 2024, steps=steps - 1)

        self.cache[cache_key] = result
        return result

    def part1(self) -> int:
        return sum(self.solve(num, steps=25) for num in self.nums)

    def part2(self) -> int:
        return sum(self.solve(num, steps=75) for num in self.nums)
