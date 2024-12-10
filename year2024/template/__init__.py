from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import os
import re
import sys
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, replace

import z3  # type: ignore[import]

from .. import utils as u

TEST_INPUT1 = r"""
TODO
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 0
PART_2_ANSWER = 0


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

    def part1(self) -> int:
        result = 0
        return result

    def part2(self) -> int:
        result = 0
        return result
