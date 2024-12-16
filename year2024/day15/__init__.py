from __future__ import annotations

from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 10092
PART_2_ANSWER = 9021


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part1_example2() -> None:
    assert (
        Solution.parse_input("""
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""").part1()
        == 2028
    )


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


def test_part2_example2() -> None:
    assert (
        Solution.parse_input("""
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
""").part2()
        == 618
    )


@dataclass(frozen=True, kw_only=True)
class Solution(u.Solution):
    grid_str: str
    directions: list[u.Delta]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        (grid_str, directions_str) = u.split_line_groups(input)
        directions = [
            u.Delta.parse_from_direction(char)
            for char in directions_str
            if not char.isspace()
        ]
        return cls(grid_str=grid_str, directions=directions)

    def try_push(
        self, grid: u.DenseGrid[str], position: u.Coord, direction: u.Delta
    ) -> dict[u.Coord, str] | None:
        result = self.try_push_helper(
            grid=grid, position=position + direction, direction=direction
        )
        if result is None:
            return None
        result2 = {k: "." if v is None else v for k, v in result.items()}
        result2[position] = "."
        result2[position + direction] = "@"
        return result2

    def try_push_helper(
        self, grid: u.DenseGrid[str], position: u.Coord, direction: u.Delta
    ) -> dict[u.Coord, str | None] | None:
        match grid[position]:
            case "#":
                return None
            case ".":
                return {}
            case "O":
                left_coord = position
                right_coord = position
            case "[":
                left_coord = position
                right_coord = position + u.Deltas2d.RIGHT
            case "]":
                left_coord = position + u.Deltas2d.LEFT
                right_coord = position
            case char:
                raise ValueError(f"unexpected character {char=}")

        updates = []
        match direction:
            case u.Deltas2d.UP | u.Deltas2d.DOWN:
                updates.append(
                    self.try_push_helper(
                        grid=grid, position=left_coord + direction, direction=direction
                    )
                )
                updates.append(
                    self.try_push_helper(
                        grid=grid, position=right_coord + direction, direction=direction
                    )
                )
                updates.append(
                    {
                        left_coord: None,
                        left_coord + direction: grid[left_coord],
                        right_coord: None,
                        right_coord + direction: grid[right_coord],
                    }
                )
            case u.Deltas2d.LEFT:
                updates.append(
                    self.try_push_helper(
                        grid=grid, position=left_coord + direction, direction=direction
                    )
                )
                updates.append(
                    {
                        left_coord + direction: grid[left_coord],
                        left_coord: grid[right_coord],
                        right_coord: None,
                    }
                )
            case u.Deltas2d.RIGHT:
                updates.append(
                    self.try_push_helper(
                        grid=grid, position=right_coord + direction, direction=direction
                    )
                )
                updates.append(
                    {
                        left_coord: None,
                        right_coord: grid[left_coord],
                        right_coord + direction: grid[right_coord],
                    }
                )
            case _:
                raise ValueError(f"unexpected direction {direction=}")

        result: dict[u.Coord, str | None] = {}
        for update in updates:
            if update is None:
                return None
            for k, v in update.items():
                if k not in result or result[k] is None:
                    result[k] = v
                elif v is not None:
                    assert result[k] == v, f"{result[k]=} {v=} {result=} {grid=}"
        return result

    def solve(self, grid: u.DenseGrid[str]) -> int:
        position = u.only_exn(grid.find("@"))
        for direction in self.directions:
            assert grid[position] == "@"
            updates = self.try_push(grid=grid, position=position, direction=direction)
            if updates is not None:
                grid.update(updates)
                position = position + direction
        return sum(
            coord.y * 100 + coord.x
            for (coord, _cell) in grid.find_where(lambda c: c in {"O", "["})
        )

    def part1(self) -> int:
        grid = u.DenseGrid.from_str(self.grid_str)
        return self.solve(grid)

    def part2(self) -> int:
        wide_grid_chars = {
            "O": "[]",
            "#": "##",
            ".": "..",
            "@": "@.",
            "\n": "\n",
        }
        grid_str = "".join(wide_grid_chars[c] for c in self.grid_str)
        grid = u.DenseGrid.from_str(grid_str)
        return self.solve(grid)
