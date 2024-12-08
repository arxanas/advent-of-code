from __future__ import annotations

import collections
import sys
from dataclasses import dataclass

from .. import utils as u

TEST_INPUT = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

PART_1_ANSWER = 64
PART_2_ANSWER = 58

Input = set[u.Coord]


def parse_input(input: str) -> Input:
    return {u.Coord(*map(int, line.split(","))) for line in input.strip().splitlines()}


def surface_area(grid: set[u.Coord], cube: u.Coord) -> int:
    result = 0
    for delta in u.Deltas3d.CARDINAL:
        if cube + delta not in grid:
            result += 1
    return result


def part1(input: Input) -> int:
    return sum(surface_area(input, cube) for cube in input)


def test_part1() -> None:
    assert part1({u.Coord(1, 1, 1), u.Coord(2, 1, 1)}) == 10
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


@dataclass
class Group:
    members: set[u.Coord]
    touches_wall: bool


def part2(input: Input) -> int:
    min_coord = u.Coord(0, 0, 0)
    assert all(min_coord.chess_distance(coord) >= 2 for coord in input)
    max_coord = u.Coord(20, 20, 20)
    assert all(max_coord.chess_distance(coord) >= 2 for coord in input)
    all_coords = set(min_coord.between(max_coord))
    assert input < all_coords

    all_seen_coords = set[u.Coord]()
    groups = list[Group]()
    for coord in all_coords:
        if coord in all_seen_coords:
            continue
        if coord in input:
            # Don't want to flood-fill the input cubes.
            continue

        members = set[u.Coord]()
        touches_wall = False
        queue = collections.deque([coord])
        while queue:
            current = queue.popleft()
            if current in all_seen_coords:
                continue
            members.add(current)
            all_seen_coords.add(current)

            for delta in u.Deltas3d.CARDINAL:
                neighbor = current + delta
                if neighbor not in all_coords:
                    touches_wall = True
                    continue
                if neighbor in input:
                    continue
                queue.append(neighbor)

        assert members <= all_seen_coords
        groups.append(Group(members=members, touches_wall=touches_wall))

    interior_cubes = set.union(
        *[group.members for group in groups if not group.touches_wall]
    )
    result = 0
    for cube in input:
        for delta in u.Deltas3d.CARDINAL:
            neighbor = cube + delta
            if neighbor in input:
                continue
            if neighbor not in interior_cubes:
                result += 1
    return result


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT)) == PART_2_ANSWER


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
