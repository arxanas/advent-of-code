import re
from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

TEST_INPUT2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

PART_1_ANSWER = 161
PART_2_ANSWER = 48


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Solution(u.Solution):
    input: str

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(input=input.strip())

    @staticmethod
    def mul(m: re.Match[str]) -> int:
        return int(m.group(1)) * int(m.group(2))

    def part1(self) -> int:
        pattern = r"mul\((\d+),(\d+)\)"
        return sum(self.mul(m) for m in re.finditer(pattern, self.input))

    def part2(self) -> int:
        pattern = r"mul\((\d+),(\d+)\)|(do)\(\)|(don't)\(\)"
        enabled = True
        result = 0
        for m in re.finditer(pattern, self.input):
            match m.group(0):
                case "do()":
                    enabled = True
                case "don't()":
                    enabled = False
                case mul:
                    assert mul.startswith("mul(")
                    if enabled:
                        result += self.mul(m)
        return result
