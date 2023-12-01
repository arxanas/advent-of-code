import sys
from functools import reduce
from typing import Iterable, Mapping, Set, Tuple

TEST_INPUT = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""

Input = Mapping[Tuple[int, int], int]


def get_adjacent(
    input: Input, row: int, col: int
) -> Iterable[Tuple[Tuple[int, int], int]]:
    for key in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
        if key in input:
            yield (key, input[key])


def get_low_points(input: Input) -> Iterable[Tuple[int, int]]:
    for (row, col), value in input.items():
        for _, adj_value in get_adjacent(input, row, col):
            if not (value < adj_value):
                break
        else:
            yield (row, col)


def part1(input: Input) -> str:
    risk_scores = []
    for (row, col), value in input.items():
        for _, adj_value in get_adjacent(input, row, col):
            if not (value < adj_value):
                break
        else:
            risk_scores.append(value + 1)
    return str(sum(risk_scores))


def get_basin(input: Input, row: int, col: int) -> Set[Tuple[int, int]]:
    basin: Set[Tuple[int, int]] = set()
    visit_basin(input, basin, row, col)
    return basin


def visit_basin(
    input: Input, visited: Set[Tuple[int, int]], row: int, col: int
) -> None:
    if (row, col) in visited:
        return

    value = input[row, col]
    if value == 9:
        return
    visited.add((row, col))

    for (adj_row, adj_col), adj_value in get_adjacent(input, row, col):
        if adj_value > value:
            visit_basin(input, visited, adj_row, adj_col)


def part2(input: Input) -> int:
    low_points = list(get_low_points(input))
    basins = []
    for row, col in low_points:
        basins.append(get_basin(input, row, col))
    top_basins = sorted(basins, key=len, reverse=True)[:3]
    return reduce(lambda x, y: x * y, (len(x) for x in top_basins))


def parse_input(input: str) -> Input:
    input = input.strip()
    result = {}
    for row, line in enumerate(input.splitlines()):
        for col, char in enumerate(line):
            result[row, col] = int(char)
    return result


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("test 2:", part2(test_input))
    print("part 1:", part1(input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
