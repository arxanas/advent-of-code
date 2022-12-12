import collections
import os
import sys
from typing import Optional

from .. import utils

TEST_INPUT = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

PART_1_ANSWER = 31
PART_2_ANSWER = 29

Input = utils.DenseGrid[str]


def parse_input(input: str) -> Input:
    return utils.DenseGrid.from_2d([list(x) for x in input.strip().splitlines()])


def value_to_int(value: str) -> int:
    if value == "S":
        return ord("a")
    elif value == "E":
        return ord("z")
    else:
        return ord(value)


def shortest_path(
    grid: Input, start_coords: set[utils.Coord], end_coord: utils.Coord
) -> int:
    best_lengths: dict[utils.Coord, int] = {coord: 0 for coord in start_coords}
    queue = collections.deque(start_coords)
    while queue:
        current_coord = queue.popleft()
        if current_coord == end_coord:
            return best_lengths[current_coord]

        current_value = grid[current_coord]
        neighbors = [
            coord
            for delta in utils.Deltas2d.CARDINAL
            if (coord := current_coord + delta) in grid
            if value_to_int(grid[coord]) - value_to_int(current_value) <= 1
        ]

        current_length = best_lengths[current_coord]
        for neighbor in neighbors:
            new_length = current_length + 1
            if new_length < best_lengths.get(neighbor, float("inf")):
                best_lengths[neighbor] = new_length
                queue.append(neighbor)
    raise ValueError("No path found")


def part1(grid: Input) -> int:
    start_coord = next(coord for (coord, value) in grid.iter_cells() if value == "S")
    end_coord = next(coord for (coord, value) in grid.iter_cells() if value == "E")
    return shortest_path(grid, {start_coord}, end_coord)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(grid: Input) -> int:
    start_coords = {
        coord
        for (coord, value) in grid.iter_cells()
        if value_to_int(value) == value_to_int("a")
    }
    end_coord = next(coord for (coord, value) in grid.iter_cells() if value == "E")
    return shortest_path(grid, start_coords, end_coord)


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
