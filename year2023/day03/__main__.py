import re
import sys
from collections import defaultdict

from .. import utils as u

TEST_INPUT1 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 4361
PART_2_ANSWER = 467835

Input = tuple[list[str], u.DenseGrid[str]]


def parse_input(input: str) -> Input:
    lines = input.strip().splitlines()
    return (lines, u.DenseGrid.from_2d([list(line) for line in lines]))


NUM_RE = re.compile(r"\d+")


def is_symbol(c: str) -> bool:
    return c != "." and not c.isdigit()


def part1(input: Input) -> int:
    (lines, grid) = input
    result = 0
    for y, line in enumerate(lines):
        for num in NUM_RE.finditer(line):
            (min_x, max_x) = num.span()
            coords = [u.Coord.from_2d(x, y) for x in range(min_x, max_x)]
            neighbor_coords = {
                coord + delta for coord in coords for delta in u.Deltas2d.ALL
            }
            if any(
                (neighbor := grid.get(neighbor_coord)) is not None
                and is_symbol(neighbor)
                for neighbor_coord in neighbor_coords
            ):
                result += int(num.group())
    return result


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT1)) == PART_1_ANSWER


def part2(input: Input) -> int:
    num_re = re.compile(r"\d+")

    (lines, grid) = input
    gear_nums = defaultdict[u.Coord, list[int]](list)
    for y, line in enumerate(lines):
        for num in num_re.finditer(line):
            (min_x, max_x) = num.span()
            coords = [u.Coord.from_2d(x, y) for x in range(min_x, max_x)]
            neighbor_coords = {
                coord + delta for coord in coords for delta in u.Deltas2d.ALL
            }
            for neighbor_coord in neighbor_coords:
                if grid.get(neighbor_coord) == "*":
                    gear_nums[neighbor_coord].append(int(num.group()))
                    break
    gears = [u.product_int(nums) for nums in gear_nums.values() if len(nums) == 2]
    return sum(gears)


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
