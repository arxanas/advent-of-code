import sys
from collections import defaultdict
from typing import *

from .. import utils as u

TEST_INPUT1 = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 110
PART_2_ANSWER = 20

Cell = Literal["#"]
Input = u.SparseGrid[Cell]


def parse_input(input: str) -> Input:
    grid = u.SparseGrid[Cell]({})
    for i, line in enumerate(input.strip().splitlines()):
        for j, c in enumerate(line):
            coord = u.Coord.from_2d(j, i)
            match c:
                case "#":
                    grid[coord] = c
                case ".":
                    pass
                case c:
                    raise ValueError(f"Invalid cell at {coord!r}: {c!r}")
    return grid


DELTAS = [
    [u.Deltas2d.NORTH, u.Deltas2d.NORTHEAST, u.Deltas2d.NORTHWEST],
    [u.Deltas2d.SOUTH, u.Deltas2d.SOUTHEAST, u.Deltas2d.SOUTHWEST],
    [u.Deltas2d.WEST, u.Deltas2d.NORTHWEST, u.Deltas2d.SOUTHWEST],
    [u.Deltas2d.EAST, u.Deltas2d.NORTHEAST, u.Deltas2d.SOUTHEAST],
]


def get_deltas(step_num: int) -> list[list[u.Delta]]:
    return DELTAS[step_num % 4 :] + DELTAS[: step_num % 4]


def step(grid: u.SparseGrid[Cell], step_num: int) -> u.SparseGrid[Cell]:
    votes: defaultdict[u.Coord, list[u.Coord]] = defaultdict(list)
    deltas = get_deltas(step_num=step_num)
    for current_cell, _ in grid.iter_cells():
        if not any(current_cell + delta in grid for delta in u.Deltas2d.ALL):
            continue
        for direction in deltas:
            if all(current_cell + delta not in grid for delta in direction):
                target_cell = current_cell + direction[0]
                votes[target_cell].append(current_cell)
                break

    next_grid = grid.copy()
    for target_cell, voters in votes.items():
        match voters:
            case [current_cell]:
                del next_grid[current_cell]
                next_grid[target_cell] = "#"
            case _:
                pass

    assert len(next_grid) == len(grid)
    return next_grid


def test_step() -> None:
    grid_strs = [
        """\
.....
..##.
..#..
.....
..##.
.....
""",
        """\
..##.
.....
..#..
...#.
..#..
.....
""",
        """\
.....
..##.
.#...
....#
.....
..#..
""",
        """\
..#..
....#
#....
....#
.....
..#..
""",
    ]
    grids = [parse_input(grid_str) for grid_str in grid_strs]
    grid = grids[0]
    for i, next_grid in enumerate(grids[1:]):
        actual_grid = step(grid, i)
        debug_deltas = "NSWE"[i % 4 :] + "NSWE"[: i % 4]
        assert actual_grid == next_grid, f"""\
On step {i!r} (deltas are {debug_deltas}):
Previous grid:
{grid.dump()}

Expected grid:
{next_grid.dump()}

Actual grid:
{actual_grid.dump()}
"""
        grid = next_grid


def part1(input: Input) -> int:
    grid = input
    for i in range(10):
        grid = step(grid, i)
    return (grid.width() * grid.height()) - len(grid)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT1)) == PART_1_ANSWER


def part2(input: Input) -> int:
    grid = input
    i = 0
    while True:
        next_grid = step(grid, i)
        if grid == next_grid:
            break
        grid = next_grid
        i += 1
    return i + 1


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT2)) == PART_2_ANSWER


def main() -> None:
    input = parse_input(sys.stdin.read())

    print("test 1:", part1(parse_input(TEST_INPUT1)))
    print("part 1:", part1(input))
    print("test 2:", part2(parse_input(TEST_INPUT2)))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
