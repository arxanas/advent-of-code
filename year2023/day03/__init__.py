import re
from collections import defaultdict

from year2023 import utils as u

PART_1_ANSWER = 4361
PART_2_ANSWER = 467835


def test_part1() -> None:
    assert (
        Solution().part1(Solution().parse_input(Solution.TEST_INPUT1)) == PART_1_ANSWER
    )


def test_part2() -> None:
    assert (
        Solution().part2(Solution().parse_input(Solution.TEST_INPUT2)) == PART_2_ANSWER
    )


Input = tuple[list[str], u.DenseGrid[str]]
NUM_RE = re.compile(r"\d+")


def is_symbol(c: str) -> bool:
    return c != "." and not c.isdigit()


class Solution(u.Solution[Input]):
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

    def parse_input(self, input: str) -> Input:
        lines = input.strip().splitlines()
        return (lines, u.DenseGrid.from_2d([list(line) for line in lines]))

    def part1(self, input: Input) -> int:
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

    def part2(self, input: Input) -> int:
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
