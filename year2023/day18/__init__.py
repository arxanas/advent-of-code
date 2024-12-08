from __future__ import annotations

import re
from dataclasses import dataclass

from year2023.utils._grid import Coord

from .. import utils as u

TEST_INPUT1 = r"""
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 62
PART_2_ANSWER = 952408144115


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Instr:
    direction: str
    length: int
    color: str


@dataclass
class Solution(u.Solution):
    instrs: list[Instr]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        LINE_RE = re.compile(r"([RLDU]) (\d+) \(#([0-9a-f]{6})\)")
        instrs = []
        for line in input.strip().splitlines():
            match = LINE_RE.fullmatch(line)
            assert match is not None
            direction, length, color = match.groups()
            instrs.append(Instr(direction, int(length), color))
        return cls(instrs=instrs)

    def part1(self) -> int:
        grid = u.SparseGrid[str]({})
        coord = u.Coord.from_2d(0, 0)
        grid[coord] = "<unset>"
        first_coord = None
        for instr in self.instrs:
            for _ in range(instr.length):
                delta = u.Delta.parse_from_direction(instr.direction)
                coord += delta
                if first_coord is None:
                    first_coord = coord
                grid[coord] = instr.color
        assert first_coord

        class FloodFill(u.FloodFill[u.Coord]):
            def get_neighbors(self, node: Coord) -> list[Coord]:
                return [
                    next_node
                    for delta in u.Deltas2d.CARDINAL
                    if (next_node := (node + delta)) not in grid
                ]

        flood_fill = FloodFill()
        inside = u.first_completed_generator(
            [
                flood_fill.run(start_nodes=[start_coord])
                for delta in u.Deltas2d.CARDINAL
                if (start_coord := (first_coord + delta)) not in grid
            ]
        )
        return len(grid) + len(inside)

    def part2(self) -> int:
        coords = [u.Coord.from_2d(0, 0)]
        outer_area = 0
        for instr in self.instrs:
            length_str, direction_char = instr.color[:5], instr.color[5:]
            length = u.hex_to_dec(length_str)
            direction = {
                "0": u.Deltas2d.RIGHT,
                "1": u.Deltas2d.DOWN,
                "2": u.Deltas2d.LEFT,
                "3": u.Deltas2d.UP,
            }[direction_char]
            delta = direction * length
            next_coord = coords[-1] + delta
            coords.append(next_coord)
            outer_area += length

        # Calculate area of polygon enclosed by above points.
        # https://en.wikipedia.org/wiki/Shoelace_formula#Triangle_formula
        area = 0
        for i in range(len(coords) - 1):
            area += coords[i].x * coords[i + 1].y
            area -= coords[i].y * coords[i + 1].x
        area = int(abs(area))
        area += outer_area
        area //= 2
        area += 1  # ???
        return area
