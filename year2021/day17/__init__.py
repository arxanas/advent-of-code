from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Iterable, Tuple

TEST_INPUT = """
target area: x=20..30, y=-10..-5
"""


@dataclass
class Target:
    x_min: int
    x_max: int
    y_min: int
    y_max: int


Input = Target


@dataclass
class Probe:
    x: int
    y: int
    dx: int
    dy: int


def step(probe: Probe) -> Probe:
    x = probe.x + probe.dx
    y = probe.y + probe.dy
    if probe.dx > 0:
        dx = probe.dx - 1
    elif probe.dx < 0:
        dx = probe.dx + 1
    else:
        dx = probe.dx
    dy = probe.dy - 1
    return Probe(x=x, y=y, dx=dx, dy=dy)


def is_in_target_area(probe: Probe, target: Target) -> bool:
    return (
        target.x_min <= probe.x <= target.x_max
        and target.y_min <= probe.y <= target.y_max
    )


def is_out_of_range(probe: Probe, target: Target) -> bool:
    return probe.y < target.y_min


def find_trajectories(target: Target) -> Iterable[Tuple[int, Probe]]:
    x_diff = abs(target.x_max) + (target.x_max - target.x_min)
    y_diff = abs(target.y_max) + (target.y_max - target.y_min)
    for dx in range(-x_diff - 1, x_diff + 2):
        for dy in range(-y_diff - 1, y_diff + 2):
            initial_probe = Probe(x=0, y=0, dx=dx, dy=dy)
            probe = initial_probe
            highest_y = 0
            while not is_out_of_range(probe, target):
                if is_in_target_area(probe, target):
                    yield (highest_y, initial_probe)
                    break
                probe = step(probe=probe)
                highest_y = max(highest_y, probe.y)


def part1(input: Input) -> str:
    target = input
    (highest_y, probe) = max(find_trajectories(target), key=lambda x: x[0])
    return str(highest_y)


def part2(input: Input) -> str:
    velocities = {(probe.dx, probe.dy) for (_, probe) in find_trajectories(input)}
    return str(len(velocities))


def parse_input(input: str) -> Input:
    (_, _, x, y) = input.split(" ")
    x = x.split("=")[1].strip(",")
    (x_min, x_max) = x.split("..")
    y = y.split("=")[1].strip(",")
    (y_min, y_max) = y.split("..")
    return Target(
        x_min=int(x_min), x_max=int(x_max), y_min=int(y_min), y_max=int(y_max)
    )


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
