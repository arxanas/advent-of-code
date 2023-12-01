import re
import sys

import z3  # type: ignore

from .. import utils as u

TEST_INPUT = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

PART_1_ANSWER = 26
PART_2_ANSWER = 56_000_011

Input = list[tuple[u.Coord, u.Coord]]


def parse_input(input: str) -> Input:
    result = []
    for line in input.strip().splitlines():
        match = re.match(
            r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )
        assert match is not None
        coord1 = u.Coord.from_2d(int(match[1]), int(match[2]))
        coord2 = u.Coord.from_2d(int(match[3]), int(match[4]))
        result.append((coord1, coord2))
    return result


def part1(input: Input, y: int = 10) -> int:
    occupied_xs: set[int] = set()
    for sensor, beacon in input:
        distance = sensor.manhattan_distance(beacon)
        remaining = distance - abs(y - sensor.y)
        occupied_xs.update(range(sensor.x - remaining, sensor.x + remaining + 1))

    sensed_beacons = (beacon.x for _, beacon in input if beacon.y == y)
    occupied_xs.difference_update(sensed_beacons)
    return len(occupied_xs)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2_z3(input: Input, max_xy: int = 20) -> int:
    # Oops, I didn't figure out a "real" solution for this part of the problem.
    x = z3.Int("x")
    y = z3.Int("y")
    solver = z3.Solver()
    solver.add(
        0 <= x,
        x <= max_xy,
        0 <= y,
        y <= max_xy,
    )
    for sensor, beacon in input:
        distance = sensor.manhattan_distance(beacon)
        solver.add(z3.Abs(x - sensor.x) + z3.Abs(y - sensor.y) > distance)  # type: ignore

    assert solver.check() == z3.sat
    result: int = solver.model().eval(x * 4_000_000 + y).as_long()  # type: ignore
    return result


def test_part2() -> None:
    assert part2_z3(parse_input(TEST_INPUT)) == PART_2_ANSWER


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input, y=2_000_000))
    print("test 2 (Z3):", part2_z3(test_input))
    print("part 2 (Z3):", part2_z3(input, max_xy=4_000_000))


if __name__ == "__main__":
    main()
