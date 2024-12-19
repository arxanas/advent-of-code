from __future__ import annotations

from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 6
PART_2_ANSWER = 16


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    cache: dict[str, int]
    patterns: list[str]
    designs: list[str]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        (patterns, designs) = u.split_line_groups(input)
        return cls(
            cache={},
            patterns=patterns.split(", "),
            designs=u.split_lines(designs),
        )

    def num_ways(self, design: str) -> int:
        if design == "":
            return 1
        if design in self.cache:
            return self.cache[design]
        result = sum(
            self.num_ways(design[len(pattern) :])
            for pattern in self.patterns
            if design.startswith(pattern)
        )
        self.cache[design] = result
        return result

    def part1(self) -> int:
        return u.count(design for design in self.designs if self.num_ways(design) > 0)

    def part2(self) -> int:
        return sum(self.num_ways(design) for design in self.designs)
