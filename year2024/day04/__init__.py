from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 18
PART_2_ANSWER = 9


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Solution(u.Solution):
    input: str
    grid: u.DenseGrid[str]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        grid = u.DenseGrid.from_str(input)
        return cls(input=input, grid=grid)

    def part1(self) -> int:
        search = "XMAS"
        result = 0
        for coord in self.grid.iter_coords():
            for cells in self.grid.iter_deltas(
                start=coord,
                deltas=u.Deltas2d.ALL,
                include_start=True,
                max_steps=len(search),
            ):
                word = "".join(cell for (_coord, cell, _delta) in cells)
                if word == search:
                    result += 1
        return result

    def part2(self) -> int:
        cross_deltas = [
            [u.Deltas2d.UP_RIGHT, u.Deltas2d.ZERO, u.Deltas2d.DOWN_LEFT],
            [u.Deltas2d.UP_LEFT, u.Deltas2d.ZERO, u.Deltas2d.DOWN_RIGHT],
            [u.Deltas2d.DOWN_RIGHT, u.Deltas2d.ZERO, u.Deltas2d.UP_LEFT],
            [u.Deltas2d.DOWN_LEFT, u.Deltas2d.ZERO, u.Deltas2d.UP_RIGHT],
        ]
        result = 0
        for center_coord in self.grid.iter_coords():
            cross_words = []
            for deltas in cross_deltas:
                word = "".join(
                    self.grid.get(center_coord + delta, "") for delta in deltas
                )
                cross_words.append(word)
            if cross_words.count("MAS") == 2:
                assert cross_words.count("SAM") == 2
                result += 1
        return result
