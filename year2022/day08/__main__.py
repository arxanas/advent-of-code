from __future__ import annotations

import sys

from .. import utils

TEST_INPUT = """
30373
25512
65332
33549
35390
"""

PART_1_ANSWER = 21
PART_2_ANSWER = 8

Input = utils.DenseGrid[int]


def parse_input(input: str) -> Input:
    rows = []
    for line in input.strip().splitlines():
        row = []
        for char in line:
            row.append(int(char))
        rows.append(row)
    return utils.DenseGrid.from_2d(rows=rows)


def is_visible_from_edge(grid: Input, start: utils.Coord) -> bool:
    for delta in utils.Deltas2d.CARDINAL:
        if all(
            value < grid[start]
            for (_, value) in grid.iter_delta(
                start=start, delta=delta, include_start=False
            )
        ):
            return True
    return False


def part1(grid: Input) -> int:
    return utils.count(
        coord for coord in grid.iter_coords() if is_visible_from_edge(grid, coord)
    )


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def calc_scenic_score(grid: Input, start: utils.Coord) -> int:
    scores = []
    for delta in utils.Deltas2d.CARDINAL:
        score = 0
        for _, value in grid.iter_delta(start=start, delta=delta, include_start=False):
            score += 1
            if value >= grid[start]:
                break
        scores.append(score)
    return utils.product_int(scores)


def part2(input: Input) -> int:
    return max(calc_scenic_score(input, coord) for coord in input.iter_coords())


def test_part2() -> None:
    grid = parse_input(TEST_INPUT)
    for coord, _ in grid.iter_edges():
        assert calc_scenic_score(grid, coord) == 0
    assert grid[utils.Coord(2, 3, 0)] == 5
    assert calc_scenic_score(grid, utils.Coord(2, 3, 0)) == 8
    assert part2(grid) == PART_2_ANSWER


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
