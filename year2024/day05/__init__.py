from collections import Counter, defaultdict
from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 143
PART_2_ANSWER = 123


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Solution(u.Solution):
    rules: list[tuple[int, int]]
    updates: list[list[int]]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        (page_rules, page_updates) = u.split_line_groups(input)
        return cls(
            rules=u.extract_int_list_pairs(page_rules),
            updates=[u.extract_int_list(line) for line in u.split_lines(page_updates)],
        )

    def satisfies_rules(self, update: list[int]) -> bool:
        for before, after in self.rules:
            try:
                before_idx = update.index(before)
                after_idx = update.index(after)
            except ValueError:
                continue
            assert before_idx != after_idx
            if before_idx > after_idx:
                return False
        return True

    def part1(self) -> int:
        result = 0
        for update in self.updates:
            if self.satisfies_rules(update):
                middle_idx = len(update) // 2
                result += update[middle_idx]
        return result

    def part2(self) -> int:
        deps = defaultdict[int, list[int]](list)
        for before, after in self.rules:
            deps[after].append(before)

        def reorder(update: list[int]) -> list[int]:
            result: list[int] = []

            def add_page(page: int) -> None:
                if page in result:
                    return
                for dep in deps[page]:
                    if dep in update:
                        add_page(dep)
                result.append(page)

            for page in update:
                add_page(page)
            return result

        result = 0
        for update in self.updates:
            if not self.satisfies_rules(update):
                reordered_update = reorder(update)
                assert Counter(update) == Counter(reordered_update)
                assert self.satisfies_rules(reordered_update)
                middle_idx = len(reordered_update) // 2
                result += reordered_update[middle_idx]
        return result
