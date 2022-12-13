import functools
import itertools
import json
import sys
from typing import Union

TEST_INPUT = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

PART_1_ANSWER = 13
PART_2_ANSWER = 140

Packet = Union[int, list["Packet"]]
Input = list[tuple[Packet, Packet]]


def parse_input(input: str) -> Input:
    result: Input = []
    for group in input.strip().split("\n\n"):
        packets = []
        for line in group.strip().splitlines():
            packets.append(json.loads(line))
        (lhs, rhs) = packets
        result.append((lhs, rhs))
    return result


def compare(lhs: Packet, rhs: Packet) -> int:
    if isinstance(lhs, list) and isinstance(rhs, list):
        for (l, r) in itertools.zip_longest(lhs, rhs):
            if l is None:
                return -1
            elif r is None:
                return 1
            else:
                comparison = compare(l, r)
                if comparison != 0:
                    return comparison
        return 0
    elif isinstance(lhs, list) and isinstance(rhs, int):
        return compare(lhs, [rhs])
    elif isinstance(lhs, int) and isinstance(rhs, list):
        return compare([lhs], rhs)
    elif isinstance(lhs, int) and isinstance(rhs, int):
        return lhs - rhs
    else:
        raise TypeError("Invalid operands: {} and {}".format(lhs, rhs))


def part1(input: Input) -> int:
    return sum(i for (i, (lhs, rhs)) in enumerate(input, 1) if compare(lhs, rhs) <= 0)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    packet1: Packet = [[2]]
    packet2: Packet = [[6]]
    all_packets: list[Packet] = [packet1, packet2]
    for (lhs, rhs) in input:
        all_packets.append(lhs)
        all_packets.append(rhs)
    all_packets.sort(key=functools.cmp_to_key(compare))
    index1 = all_packets.index(packet1) + 1
    index2 = all_packets.index(packet2) + 1
    return index1 * index2


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
