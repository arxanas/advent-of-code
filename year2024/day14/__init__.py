from __future__ import annotations

from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 12


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    # This answer isn't meaningful, it's just the first value for which the
    # heuristic works in the provided test case:
    assert Solution.parse_input(TEST_INPUT2).part2() == 22


@dataclass
class Robot:
    GRID_WIDTH = 101
    GRID_HEIGHT = 103

    position: u.Coord
    velocity: u.Delta

    @classmethod
    def parse(cls, line: str) -> Robot:
        ((x, y), (dx, dy)) = u.extract_int_list_pairs(line)
        return cls(position=u.Coord.from_2d(x, y), velocity=u.Delta.from_2d(dx, dy))

    def step(self) -> Robot:
        position = self.position + self.velocity
        position = u.Coord.from_2d(
            position.x % self.GRID_WIDTH, position.y % self.GRID_HEIGHT
        )
        return Robot(position=position, velocity=self.velocity)

    def quadrant(self) -> tuple[int, int] | None:
        if (
            self.position.x == Robot.GRID_WIDTH // 2
            or self.position.y == Robot.GRID_HEIGHT // 2
        ):
            return None
        quadrant_x = self.position.x >= self.GRID_WIDTH // 2
        quadrant_y = self.position.y >= self.GRID_HEIGHT // 2
        return int(quadrant_x), int(quadrant_y)

    def is_in_center(self) -> bool:
        margin = 15
        return (
            margin <= self.position.x <= self.GRID_WIDTH - margin
            and margin <= self.position.y <= self.GRID_HEIGHT - margin
        )


@dataclass
class Solution(u.Solution):
    robots: list[Robot]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        return cls(robots=[Robot.parse(line) for line in u.split_lines(input)])

    def part1(self) -> int:
        robots = list(self.robots)
        for _ in range(100):
            robots = [robot.step() for robot in robots]

        quadrant_to_robots = u.group_by(
            (quadrant, robot)
            for robot in self.robots
            if (quadrant := robot.quadrant()) is not None
        )
        return u.product_int(len(quadrant) for quadrant in quadrant_to_robots.values())

    def part2(self) -> int:
        robots = list(self.robots)
        for i in range(1, 20_000):
            robots = [robot.step() for robot in robots]
            center_robots = [robot for robot in robots if robot.is_in_center()]
            if len(center_robots) >= 0.8 * len(robots):
                # For debugging:
                # print(f"{i=}")
                # print(u.SparseGrid[str]({robot.position: "#" for robot in robots}))
                return i
        raise RuntimeError("no christmas tree found")
