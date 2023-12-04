from functools import *
from itertools import *

from .. import utils as u

Card = tuple[frozenset[int], frozenset[int]]
Input = list[Card]

TEST_INPUT1 = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 13
PART_2_ANSWER = 30


def test_part1() -> None:
    assert Solution().part1(Solution().parse_input(TEST_INPUT1)) == PART_1_ANSWER


def test_part2() -> None:
    assert Solution().part2(Solution().parse_input(TEST_INPUT2)) == PART_2_ANSWER


class Solution(u.Solution[Input]):
    def parse_input(self, input: str) -> Input:
        def parse_num_list(s: str) -> frozenset[int]:
            return frozenset(int(x) for x in s.split())

        lines = input.strip().splitlines()
        result = []
        for line in lines:
            line = line.split(":")[1]
            (first, second) = line.split("|")
            result.append((parse_num_list(first), parse_num_list(second)))
        return result

    def part1(self, input: Input) -> int:
        result = 0
        for first, second in input:
            common = first & second
            if common:
                result += 2 ** (len(common) - 1)
        return result

    def part2(self, input: Input) -> int:
        @cache
        def process_card(index: int, card: Card) -> int:
            (first, second) = card
            common = first & second
            new_indexes = [index + i + 1 for i in range(len(common))]
            return 1 + sum(process_card(i, input[i]) for i in new_indexes)

        return sum(process_card(i, card) for i, card in enumerate(input))
