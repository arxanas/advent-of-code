import itertools
import operator
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import TypeAlias

from .. import utils as u

TEST_INPUT1 = r"""
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 3749
PART_2_ANSWER = 11387


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


Operator: TypeAlias = Callable[[int, int], int]
OperatorSet: TypeAlias = Sequence[Operator]


@dataclass
class Equation:
    result: int
    operands: list[int]

    @classmethod
    def from_line(cls, line: str) -> "Equation":
        [result, *operands] = u.extract_int_list(line)
        return cls(result=result, operands=operands)

    def _apply_operators(self, operators: Sequence[Operator]) -> int:
        assert self.operands
        [result, *operands] = self.operands
        assert len(operands) == len(operators)
        for operand, f in zip(operands, operators):
            result = f(result, operand)
        return result

    def can_solve(self, operator_set: OperatorSet) -> bool:
        return any(
            self._apply_operators(ops) == self.result
            for ops in itertools.product(operator_set, repeat=len(self.operands) - 1)
        )


PART1_OPS: OperatorSet = [operator.add, operator.mul]
PART2_OPS: OperatorSet = [
    operator.add,
    operator.mul,
    lambda x, y: int(str(x) + str(y)),
]


def test_can_solve() -> None:
    assert not Equation(result=1, operands=[2]).can_solve(operator_set=PART1_OPS)
    assert Equation(result=1, operands=[1]).can_solve(operator_set=PART1_OPS)
    assert Equation(result=5, operands=[2, 3]).can_solve(operator_set=PART1_OPS)
    assert Equation(result=3267, operands=[81, 40, 27]).can_solve(
        operator_set=PART1_OPS
    )
    assert Equation(result=7290, operands=[6, 8, 6, 15]).can_solve(
        operator_set=PART2_OPS
    )


@dataclass
class Solution(u.Solution):
    equations: list[Equation]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(
            equations=[Equation.from_line(line) for line in u.split_lines(input)]
        )

    def part1(self) -> int:
        return sum(
            equation.result
            for equation in self.equations
            if equation.can_solve(operator_set=PART1_OPS)
        )

    def part2(self) -> int:
        return sum(
            equation.result
            for equation in self.equations
            if equation.can_solve(operator_set=PART2_OPS)
        )
