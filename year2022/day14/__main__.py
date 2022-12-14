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
            if lhs.x == rhs.x:
                start_y, end_y = sorted((lhs.y, rhs.y))
                for y in range(start_y, end_y + 1):
                    grid.add(u.Coord.from_2d(lhs.x, y))
            elif lhs.y == rhs.y:
                start_x, end_x = sorted((lhs.x, rhs.x))
                for x in range(start_x, end_x + 1):
                    grid.add(u.Coord.from_2d(x, lhs.y))
            else:
                raise ValueError(f"Invalid line: {lhs!r} -> {rhs!r}")
    return grid


def part1(input: Input) -> int:
    grid = {coord: "#" for coord in draw_lines(input)}
    start = u.Coord.from_2d(500, 0)
    result = 0
    floor_y = 10000
    while True:
        next = find_dest(set(grid.keys()), start, floor_y=floor_y)
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
        next = current + u.Deltas2d.SOUTH
        if next in grid:
            next = current + u.Deltas2d.SOUTHWEST
            if next in grid:
                next = current + u.Deltas2d.SOUTHEAST
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
    queue = [start]
    while queue:
        next = queue.pop()
        if next in grid or next.y >= floor_y:
            continue

        grid[next] = "o"
        result += 1
        queue.append(next + u.Deltas2d.SOUTH)
        queue.append(next + u.Deltas2d.SOUTHEAST)
        queue.append(next + u.Deltas2d.SOUTHWEST)
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
