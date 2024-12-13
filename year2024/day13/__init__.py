from __future__ import annotations

from dataclasses import dataclass

import z3
from pystreamapi import Stream

from .. import utils as u

TEST_INPUT1 = r"""
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 480
PART_2_ANSWER = 875318608908


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Machine:
    A_COST = 3
    B_COST = 1

    a: u.Delta
    b: u.Delta
    dest: u.Coord

    @classmethod
    def parse(cls, text: str) -> Machine:
        (a_x, a_y, b_x, b_y, dest_x, dest_y) = u.extract_int_list(text)
        return cls(
            a=u.Delta.from_2d(x=a_x, y=a_y),
            b=u.Delta.from_2d(x=b_x, y=b_y),
            dest=u.Coord.from_2d(x=dest_x, y=dest_y),
        )

    def required_tokens(self, dest_offset: int) -> int:
        x = z3.Int("x")
        y = z3.Int("y")
        o = z3.Optimize()
        o.add(self.a.x * x + self.b.x * y == self.dest.x + dest_offset)
        o.add(self.a.y * x + self.b.y * y == self.dest.y + dest_offset)
        o.add(x >= 0)
        o.add(y >= 0)

        o.minimize(self.A_COST * x + self.B_COST * y)
        if o.check() != z3.sat:
            return 0
        else:
            m = o.model()
            return self.A_COST * m[x].as_long() + self.B_COST * m[y].as_long()


@dataclass
class Solution(u.Solution):
    machines: list[Machine]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(
            machines=Stream.of(u.split_line_groups(input)).map(Machine.parse).to_list()
        )

    def part1(self) -> int:
        return (
            Stream.of(self.machines)
            .map(lambda machine: machine.required_tokens(dest_offset=0))
            .numeric()
            .sum()
        )

    def part2(self) -> int:
        return (
            Stream.of(self.machines)
            .map(lambda machine: machine.required_tokens(dest_offset=10000000000000))
            .numeric()
            .sum()
        )
