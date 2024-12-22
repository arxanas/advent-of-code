from __future__ import annotations

import itertools
from collections.abc import Iterable
from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
1
10
100
2024
"""

TEST_INPUT2 = """
1
2
3
2024
"""

PART_1_ANSWER = 37327623
PART_2_ANSWER = 23


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


def mix(secret: int, value: int) -> int:
    return secret ^ value


def prune(secret: int) -> int:
    return secret % 16777216


def step(secret: int) -> int:
    """
    >>> step(123)
    15887950
    """
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret


def steps(secret: int) -> Iterable[int]:
    while True:
        yield secret
        secret = step(secret)


def prices(secret: int) -> Iterable[int]:
    """
    >>> list(u.take(10, prices(123)))
    [3, 0, 6, 5, 4, 4, 6, 4, 4, 2]
    """
    for value in steps(secret):
        yield value % 10


def analyze_prices(prices: Iterable[int]) -> dict[tuple[int, ...], int]:
    result = {}
    for last_prices in u.sliding_windows(prices, 5):
        last_changes = tuple(
            [rhs - lhs for lhs, rhs in u.sliding_windows(last_prices, 2)]
        )
        if last_changes not in result:
            result[last_changes] = last_prices[-1]
    return result


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    secrets: list[int]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(secrets=u.extract_int_list(input))

    def part1(self) -> int:
        return sum(u.nth(2000, steps(secret)) for secret in self.secrets)

    def part2(self) -> int:
        analyses = [
            analyze_prices(u.take(2000, prices(secret))) for secret in self.secrets
        ]

        def evaluate(sequence: tuple[int, ...]) -> int:
            return sum(analysis.get(sequence, 0) for analysis in analyses)

        seqs = set(
            itertools.chain.from_iterable(analysis.keys() for analysis in analyses)
        )
        return max(evaluate(seq) for seq in seqs)
