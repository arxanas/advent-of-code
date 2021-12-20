import sys
from collections import *
from functools import *
from typing import *
from dataclasses import dataclass
import math

TEST_INPUT = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""


Input = Any


def add_number_to_left(val: Input, summand: int) -> Optional[Input]:
    if isinstance(val, int):
        return val + summand
    else:
        (l, r) = val
        val2 = add_number_to_left(r, summand)
        if val2 is not None:
            return [l, val2]
        add_number_to_left(l, summand)


def add_number_to_right(val: Input, summand: int) -> Optional[Input]:
    if isinstance(val, int):
        return val + summand
    else:
        (l, r) = val
        val2 = add_number_to_right(l, summand)
        if val2 is not None:
            return [val2, r]
        add_number_to_right(r, summand)


@dataclass
class AddToLeft:
    val: int


@dataclass
class AddToRight:
    val: int


@dataclass
class Done:
    pass


Directive = Union[AddToLeft, AddToRight, Done]


def explode(val: Input, depth: int) -> Tuple[Input, Optional[Directive]]:
    if isinstance(val, int):
        return (val, None)

    (l, r) = val
    if depth >= 3:
        if isinstance(l, list):
            (l2, r2) = l
            return ([0, add_number_to_right(r, r2)], AddToLeft(l2))
        elif isinstance(r, list):
            (l2, r2) = r
            return ([add_number_to_left(l, l2), 0], AddToRight(r2))

    (l, directive) = explode(l, depth=depth + 1)
    if directive is not None:
        if isinstance(directive, (AddToLeft, Done)):
            return ([l, r], directive)
        elif isinstance(directive, AddToRight):
            return ([l, add_number_to_right(r, directive.val)], Done())

    (r, directive) = explode(r, depth=depth + 1)
    if directive is not None:
        if isinstance(directive, AddToLeft):
            return ([add_number_to_left(l, directive.val), r], Done())
        elif isinstance(directive, (AddToRight, Done)):
            return ([l, r], directive)

    return ([l, r], None)


def test_explode() -> None:
    def explode_for_test(val: Input) -> Tuple[Input, bool]:
        (result, _directive) = explode(val, depth=0)
        return result

    assert explode_for_test([[[[[9, 8], 1], 2], 3], 4]) == [[[[0, 9], 2], 3], 4]
    assert explode_for_test([7, [6, [5, [4, [3, 2]]]]]) == [7, [6, [5, [7, 0]]]]
    assert explode_for_test([[6, [5, [4, [3, 2]]]], 1]) == [[6, [5, [7, 0]]], 3]
    assert explode_for_test([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]) == [
        [3, [2, [8, 0]]],
        [9, [5, [4, [3, 2]]]],
    ]
    assert explode_for_test([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]) == [
        [3, [2, [8, 0]]],
        [9, [5, [7, 0]]],
    ]


def split(val: Input) -> Tuple[Input, bool]:
    if isinstance(val, int):
        if val >= 10:
            l = math.floor(val / 2)
            r = math.ceil(val / 2)
            return ([l, r], True)
        else:
            return (val, False)
    else:
        (l, r) = val
        (l, stop) = split(l)
        if stop:
            return ([l, r], stop)

        (r, stop) = split(r)
        return ([l, r], stop)


def test_split() -> None:
    def split_for_test(val: Input) -> Input:
        (val, _stop) = split(val)
        return val

    assert split_for_test(10) == [5, 5]
    assert split_for_test(11) == [5, 6]
    assert split_for_test(12) == [6, 6]
    assert split_for_test([10, 10]) == [[5, 5], 10]
    assert split_for_test([[5, 5], 10]) == [
        [
            5,
            5,
        ],
        [5, 5],
    ]


def magnitude(val: Input) -> int:
    if isinstance(val, int):
        return val
    else:
        (l, r) = val
        return magnitude(l) * 3 + magnitude(r) * 2


def test_magnitude() -> None:
    assert magnitude([[9, 1], [1, 9]]) == 129
    assert (
        magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]])
        == 3488
    )


def add(l: Input, r: Input) -> Input:
    input = [l, r]
    while True:
        (input, directive) = explode(input, depth=0)
        if directive is not None:
            continue
        (input, made_change) = split(input)
        if made_change:
            continue
        return input


def test_add() -> None:
    # assert add([[[[4,3],4],4],[7,[[8,4],9]]], [1,1]) == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
    assert add(
        [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
        [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
    ) == [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]]


def part1(input: Input) -> str:
    added = reduce(add, input)
    return str(magnitude(added))

def part2(input: Input) -> str:
    biggest = max(magnitude(add(l, r)) for l in input for r in input if l != r)
    return str(biggest)


def parse_input(input: str) -> Input:
    return [eval(x) for x in input.strip().splitlines()]


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
