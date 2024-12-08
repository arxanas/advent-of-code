from __future__ import annotations

import sys
from typing import List, Set, Tuple

TEST_INPUT = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

Input = Tuple[List[Tuple[int, int]], List[Tuple[str, int]]]


def fold_along(grid: Set[Tuple[int, int]], dim: str, line: int) -> Set[Tuple[int, int]]:
    result = set()
    for x, y in grid:
        if dim == "x":
            if x >= line:
                x = line - (x - line)
        elif dim == "y":
            if y >= line:
                y = line - (y - line)
        else:
            raise ValueError(f"bad dim: {dim}")

        result.add((x, y))
    return result


def print_grid(grid: Set[Tuple[int, int]]) -> None:
    for y in range(max(i[1] for i in grid) + 1):
        for x in range(max(i[0] for i in grid) + 1):
            if (x, y) in grid:
                sys.stdout.write("#")
            else:
                sys.stdout.write(".")
        sys.stdout.write("\n")


def part1(input: Input) -> str:
    (points, folds) = input
    grid = set(points)
    [(dim1, line1), *_] = folds
    s = fold_along(grid, dim=dim1, line=line1)
    return str(len(s))


def part2(input: Input) -> str:
    (points, folds) = input
    grid = set(points)
    for dim, line in folds:
        grid = fold_along(grid, dim=dim, line=line)  # type: ignore[assignment]
    print_grid(grid)
    return "(see above)"


def parse_input(input: str) -> Input:
    coords = []
    folds = []
    is_coord = True
    for line in input.strip().splitlines():
        if line == "":
            is_coord = False
        elif is_coord:
            (x, y) = line.split(",")
            coords.append((int(x), int(y)))
        else:
            (_fold, _along, value) = line.split(" ")
            (dim, value) = value.split("=")
            assert dim in ["x", "y"]
            folds.append((dim, int(value)))
    return (coords, folds)


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print_grid(set(test_input[0]))
    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
