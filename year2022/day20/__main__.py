from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TypeVar

from .. import utils as u

TEST_INPUT = """
1
2
-3
3
-2
0
4
"""

PART_1_ANSWER = 3
PART_2_ANSWER = 1623178306


@dataclass(frozen=True, eq=True)
class Elem:
    index: int
    value: int


Input = list[Elem]


def parse_input(input: str) -> Input:
    result = []
    for i, line in enumerate(input.strip().splitlines()):
        result.append(Elem(index=i, value=int(line)))
    return result


T = TypeVar("T")


def move_one(input: list[Elem], elem: Elem) -> list[Elem]:
    result = list(input)
    index = result.index(elem)
    result.remove(elem)
    if not result:
        result.append(elem)
    else:
        insert_idx = (index + elem.value) % len(result)
        result.insert(insert_idx, elem)
    return result


def mix(order: Input, input: Input) -> Input:
    input = list(input)
    for elem in order:
        input = move_one(input, elem=elem)
    return input


def get_coords(input: Input) -> int:
    start_index = u.only_exn(i for (i, x) in enumerate(input) if x.value == 0)
    return (
        input[(start_index + 1000) % len(input)].value
        + input[(start_index + 2000) % len(input)].value
        + input[(start_index + 3000) % len(input)].value
    )


def part1(input: Input) -> int:
    order = list(input)
    input = mix(order=order, input=input)
    return get_coords(input)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    input = [Elem(index=elem.index, value=elem.value * 811589153) for elem in input]
    order = list(input)
    for _ in range(10):
        input = mix(order=order, input=input)
    return get_coords(input)


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
