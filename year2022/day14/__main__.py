import sys
from typing import Optional

from .. import utils as u

TEST_INPUT = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

PART_1_ANSWER = 24
PART_2_ANSWER = 93

Rock = list[u.Coord]
Input = list[Rock]


def parse_input(input: str) -> Input:
    result = []
    for line in input.strip().splitlines():
        rock = []
        for coord in line.split(" -> "):
            x, y = coord.split(",")
            rock.append(u.Coord.from_2d(int(x), int(y)))
        result.append(rock)
    return result


def draw_lines(input: Input) -> set[u.Coord]:
    grid: set[u.Coord] = set()
    for rock in input:
        for lhs, rhs in zip(rock, rock[1:]):
            for coord in lhs.between(rhs):
                grid.add(coord)
    return grid


def part1(input: Input) -> int:
    grid = {coord: "#" for coord in draw_lines(input)}
    result = 0
    while True:
        next = find_dest(set(grid.keys()), start=u.Coord.from_2d(500, 0), floor_y=10000)
        if next is None:
            break
        grid[next] = "o"
        result += 1
    return result


def print_grid(grid: dict[u.Coord, str]) -> None:
    xs = [coord.x for coord in grid.keys()]
    print("\t" + "".join(str(x % 10) for x in range(min(xs), max(xs) + 1)))
    ys = [coord.y for coord in grid.keys()]
    for y in range(min(ys), max(ys) + 1):
        line = [
            grid.get(u.Coord.from_2d(x, y), " ") for x in range(min(xs), max(xs) + 1)
        ]
        print(str(y) + "\t" + "".join(line))
    print("-" * (max(xs) - min(xs) + 1))


def find_dest(grid: set[u.Coord], start: u.Coord, floor_y: int) -> Optional[u.Coord]:
    assert start not in grid
    current = start
    while True:
        next = current.south()
        if next in grid:
            next = current.south().west()
            if next in grid:
                next = current.south().east()
                if next in grid:
                    break
        if next.y == floor_y:
            return None
        current = next
    return current


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    grid = {coord: "#" for coord in draw_lines(input)}
    start = u.Coord.from_2d(500, 0)
    floor_y = max(coord.y for coord in grid.keys()) + 2

    result = 0
    stack = [start]
    while stack:
        next = stack.pop()
        if next in grid or next.y >= floor_y:
            continue

        grid[next] = "o"
        result += 1
        stack.append(next.south())
        stack.append(next.south().east())
        stack.append(next.south().west())
    return result


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
