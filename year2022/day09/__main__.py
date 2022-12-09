import sys

from .. import utils

TEST_INPUT = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

PART_1_ANSWER = 13
PART_2_ANSWER = 1

TEST_INPUT_2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

PART_2_ANSWER_2 = 36

Input = list[tuple[str, int]]


def parse_input(input: str) -> Input:
    result = []
    for line in input.strip().splitlines():
        direction, distance = line.split()
        result.append((direction, int(distance)))
    return result


def move_towards(head_pos: utils.Coord, tail_pos: utils.Coord) -> utils.Coord:
    delta = head_pos - tail_pos
    if delta.chess_distance() > 1:
        (x_dist, y_dist) = delta.to_2d()
        x_dist = utils.clamp_int(x_dist, -1, 1)
        y_dist = utils.clamp_int(y_dist, -1, 1)
        delta = utils.Delta.from_2d(x_dist, y_dist)
        tail_pos = tail_pos + delta
    return tail_pos


def part1(input: Input) -> int:
    head_pos = utils.Coord.from_2d(0, 0)
    tail_pos = utils.Coord.from_2d(0, 0)
    seen_locations: set[utils.Coord] = {tail_pos}
    for (direction, distance) in input:
        delta = utils.Delta.parse_from_direction(direction)
        for _ in range(distance):
            head_pos += delta
            tail_pos = move_towards(head_pos, tail_pos)
            seen_locations.add(tail_pos)
    return len(seen_locations)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    head_pos = utils.Coord.from_2d(0, 0)
    tail: list[utils.Coord] = [utils.Coord.from_2d(0, 0)] * 9
    seen_locations: set[utils.Coord] = {tail[-1]}
    for (direction, distance) in input:
        delta = utils.Delta.parse_from_direction(direction)
        for _ in range(distance):
            head_pos += delta
            towards_pos = head_pos
            for i in range(len(tail)):
                tail[i] = move_towards(towards_pos, tail[i])
                towards_pos = tail[i]
            seen_locations.add(tail[-1])
    return len(seen_locations)


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT)) == PART_2_ANSWER
    assert part2(parse_input(TEST_INPUT_2)) == PART_2_ANSWER_2


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
