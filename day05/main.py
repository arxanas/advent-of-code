import sys
from typing import Dict, Iterable, List, Optional, Sequence
from dataclasses import dataclass
from collections import Counter


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True, eq=True)
class LineSegment:
    start: Point
    end: Point


def parse_input(input: str) -> Iterable[LineSegment]:
    for line in input.strip().splitlines():
        (first_str, second_str) = line.split(" -> ")
        (first_x_str, first_y_str) = first_str.split(",")
        first_x = int(first_x_str)
        first_y = int(first_y_str)
        first = Point(x=first_x, y=first_y)
        (second_x_str, second_y_str) = second_str.split(",")
        second_x = int(second_x_str)
        second_y = int(second_y_str)
        second = Point(x=second_x, y=second_y)
        yield LineSegment(start=first, end=second)


def test_parse_input() -> None:
    assert list(
        parse_input(
            """
1,2 -> 3,4
5,6 -> 7,8
"""
        )
    ) == [
        LineSegment(start=Point(x=1, y=2), end=Point(x=3, y=4)),
        LineSegment(start=Point(x=5, y=6), end=Point(x=7, y=8)),
    ]


def get_covered_points_hv(line: LineSegment) -> Iterable[Point]:
    if line.start.x == line.end.x:
        (s, e) = sorted([line.start.y, line.end.y])
        for y in range(s, e + 1):
            yield Point(x=line.start.x, y=y)
    elif line.start.y == line.end.y:
        (s, e) = sorted([line.start.x, line.end.x])
        for x in range(s, e + 1):
            yield Point(x=x, y=line.start.y)


def test_get_covered_points_hv() -> None:
    assert set(
        get_covered_points_hv(LineSegment(start=Point(x=3, y=3), end=Point(x=1, y=3)))
    ) == {Point(x=1, y=3), Point(x=2, y=3), Point(x=3, y=3)}

TEST_INPUT = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

def part1(line_segments: Iterable[LineSegment]) -> int:
    graph: Dict[Point, int] = Counter()
    for line in line_segments:
        for point in get_covered_points_hv(line):
            graph[point] += 1
    return len([k for (k, v) in graph.items() if v > 1])

def test_part1() -> None:
    line_segments = parse_input(TEST_INPUT)
    assert part1(line_segments) == 5

def get_covered_points_hvd(line: LineSegment) -> Iterable[Point]:
    if line.start.x == line.end.x:
        (s, e) = sorted([line.start.y, line.end.y])
        for y in range(s, e + 1):
            yield Point(x=line.start.x, y=y)
    elif line.start.y == line.end.y:
        (s, e) = sorted([line.start.x, line.end.x])
        for x in range(s, e + 1):
            yield Point(x=x, y=line.start.y)
    else:
        (smaller_x , larger_x) = sorted([line.start, line.end], key=lambda point: point.x)
        if smaller_x.y < larger_x.y:
            step = 1
        else:
            step = -1

        for (i, x) in enumerate(range(smaller_x.x, larger_x.x + 1)):
            y = smaller_x.y + (i * step)
            yield Point(x=x, y=y)


def test_get_covered_points_hvd() -> None:
    assert set(get_covered_points_hvd(LineSegment(start=Point(x=9, y=7), end=Point(x=7, y=9)))) == {
        Point(x=9, y=7),
        Point(x=8, y=8),
        Point(x=7, y=9),
    }


def part2(line_segments: Iterable[LineSegment]) -> int:
    graph: Dict[Point, int] = Counter()
    for line in line_segments:
        for point in get_covered_points_hvd(line):
            graph[point] += 1
    return len([k for (k, v) in graph.items() if v > 1])

def test_part2() -> None:
    line_segments = parse_input(TEST_INPUT)
    assert part2(line_segments) == 12

def main() -> None:
    input = sys.stdin.read()
    line_segments = list(parse_input(input))
    print("part 1:", part1(line_segments))
    print("part 2:", part2(line_segments))


if __name__ == "__main__":
    main()
