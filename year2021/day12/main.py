import sys
import copy
from collections import *
from functools import *
from typing import *

TEST_INPUT = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""

Input = Dict[str, List[str]]


def find_paths(
    input: Input, current: str, visited_small_caves: Set[str], path: List[str]
):
    if current == "end":
        yield path
    for next_node in input[current]:
        if next_node == "start":
            continue
        if next_node not in visited_small_caves:
            if next_node.islower():
                visited_small_caves.add(next_node)
            yield from find_paths(
                input, next_node, visited_small_caves, path + [next_node]
            )
            if next_node.islower():
                visited_small_caves.remove(next_node)


def part1(input: Input) -> str:
    num_paths = len(
        list(find_paths(input, current="start", visited_small_caves=set(), path=[]))
    )
    # for path in list(find_paths(input, current="start", visited_small_caves=set(), path=["start"])):
    #     print(",".join(path))
    return str(num_paths)


def find_paths2(
    input: Input, current: str, visited_small_caves: Set[str], extra_cave: Optional[str], path: List[str]
):
    if current == "end":
        yield path
    for next_node in input[current]:
        if next_node == "start":
            continue
        if next_node not in visited_small_caves:
            if next_node.islower():
                visited_small_caves.add(next_node)
            yield from find_paths2(
                input, next_node, visited_small_caves, extra_cave, path + [next_node]
            )
            if next_node.islower():
                visited_small_caves.remove(next_node)
        elif next_node != "end" and next_node.islower() and extra_cave is None:
            yield from find_paths2(
                input, next_node, visited_small_caves, next_node, path + [next_node]
            )


def part2(input: Input) -> str:
    num_paths = len(
        list(find_paths2(input, current="start", visited_small_caves=set(), extra_cave=None, path=[]))
    )
    # for path in list(find_paths(input, current="start", visited_small_caves=set(), path=["start"])):
    #     print(",".join(path))
    return str(num_paths)
    return ""


def parse_input(input: str) -> Input:
    nodes = defaultdict(list)
    for line in input.strip().splitlines():
        (a, b) = line.split("-")
        nodes[a].append(b)
        nodes[b].append(a)
    return nodes


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
