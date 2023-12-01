import sys
from collections import Counter
from functools import lru_cache
from typing import Dict, List, Tuple

TEST_INPUT = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

Input = Tuple[str, List[Tuple[str, str]]]


def rewrite_one(formula: str, rules: List[Tuple[str, str]]) -> str:
    insertions = {}
    for i, (a, b) in enumerate(zip(formula, formula[1:])):
        for before, after in rules:
            if a + b == before:
                insertions[i] = after
    result = ""
    for i, c in enumerate(formula):
        result += c
        if i in insertions:
            result += insertions[i]
    return result


def part1(input: Input) -> str:
    (formula, rules) = input
    for i in range(10):
        formula = rewrite_one(formula, rules)

    elements = Counter(formula)
    [(lc_v, least_common), *_, (mc_v, most_common)] = sorted(
        (v, k) for (k, v) in elements.items()
    )
    return str(mc_v - lc_v)


def merge_counters(c1: Dict[str, int], c2: Dict[str, int]) -> Dict[str, int]:
    result: Counter[str] = Counter()
    for k, v in c1.items():
        result[k] += v
    for k, v in c2.items():
        result[k] += v
    return result


def part2(input: Input) -> str:
    (formula, rules) = input
    rewrite_rules = {}
    for k, v in rules:
        rewrite_rules[k] = k[0] + v + k[1]

    rules2 = dict(rules)

    @lru_cache(maxsize=None)
    def rewrite(segment: str, depth: int) -> Dict[str, int]:
        assert len(segment) == 2
        if depth == 0 or segment not in rules2:
            return Counter()
        else:
            n = rules2[segment]
            ns1 = segment[0] + n
            ns2 = n + segment[1]
            ns1c = rewrite(ns1, depth - 1)
            ns2c = rewrite(ns2, depth - 1)
            result = merge_counters(ns1c, ns2c)
            result[n] += 1
            return result

    result: Dict[str, int] = Counter(formula)
    for a, b in zip(formula, formula[1:]):
        segment = a + b
        result = merge_counters(result, rewrite(segment, 40))
    [(lc_v, least_common), *_, (mc_v, most_common)] = sorted(
        (v, k) for (k, v) in result.items()
    )
    print(least_common, lc_v)
    print(most_common, mc_v)
    return str(mc_v - lc_v)


def parse_input(input: str) -> Input:
    (formula, b) = input.strip().split("\n\n")
    rules = []
    for line in b.splitlines():
        (c, d) = line.split(" -> ")
        rules.append((c, d))
    return (formula, rules)


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
