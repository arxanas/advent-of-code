import copy
import sys
from dataclasses import dataclass

from .. import utils

TEST_INPUT = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

PART_1_ANSWER = 10605
PART_2_ANSWER = 2713310158


@dataclass
class Monkey:
    items: list[int]
    operation: str
    divisibility: int
    if_true_throw: int
    if_false_throw: int
    inspection_count: int


Input = list[Monkey]


def parse_input(input: str) -> Input:
    result = []
    for group in input.strip().split("\n\n"):
        [_, items, operation, test, iftrue, iffalse] = group.strip().split("\n")
        items2 = items.split(": ")[1].split(", ")
        [_, operation2] = operation.split("new = ")
        [_, test] = test.split("by ")
        [_, iftrue] = iftrue.split("monkey ")
        [_, iffalse] = iffalse.split("monkey ")
        result.append(
            Monkey(
                items=[int(item) for item in items2],
                operation=operation2,
                divisibility=int(test),
                if_true_throw=int(iftrue),
                if_false_throw=int(iffalse),
                inspection_count=0,
            )
        )
    return result


def part1(input: Input) -> int:
    monkeys = copy.deepcopy(input)
    for _ in range(20):
        for i, monkey in enumerate(monkeys):
            for item in monkey.items:
                monkey.inspection_count += 1
                match monkey.operation.split(" "):
                    case [_, "+", "old"]:
                        new = item + int(item)
                    case [_, "*", "old"]:
                        new = item * int(item)
                    case [_, "+", num]:
                        new = item + int(num)
                    case [_, "*", num]:
                        new = item * int(num)
                    case operation:
                        raise Exception(f"Unknown operation: {operation!r}")
                new //= 3
                if new % monkey.divisibility == 0:
                    monkeys[monkey.if_true_throw].items.append(new)
                else:
                    monkeys[monkey.if_false_throw].items.append(new)
            monkey.items = []

    active_monkeys = sorted(monkeys, key=lambda m: m.inspection_count, reverse=True)
    top_monkeys = [m.inspection_count for m in active_monkeys[:2]]
    return utils.product_int(top_monkeys)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    monkeys = copy.deepcopy(input)
    divisors = [monkey.divisibility for monkey in monkeys]
    divisor = utils.product_int(divisors)
    for _ in range(10000):
        for i, monkey in enumerate(monkeys):
            for item in monkey.items:
                monkey.inspection_count += 1
                match monkey.operation.split(" "):
                    case [_, "+", "old"]:
                        new = item + int(item)
                    case [_, "*", "old"]:
                        new = item * int(item)
                    case [_, "+", num]:
                        new = item + int(num)
                    case [_, "*", num]:
                        new = item * int(num)
                    case operation:
                        raise Exception(f"Unknown operation: {operation!r}")
                new %= divisor
                if new % monkey.divisibility == 0:
                    monkeys[monkey.if_true_throw].items.append(new)
                else:
                    monkeys[monkey.if_false_throw].items.append(new)
            monkey.items = []

    active_monkeys = sorted(monkeys, key=lambda m: m.inspection_count, reverse=True)
    top_monkeys = [m.inspection_count for m in active_monkeys[:2]]
    return utils.product_int(top_monkeys)


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT)) == PART_2_ANSWER


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
