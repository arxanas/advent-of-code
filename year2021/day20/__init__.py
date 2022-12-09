import sys
from typing import Dict, List, Tuple

TEST_INPUT = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


Point = Tuple[int, int]
Image = Tuple[bool, Dict[Point, bool]]
Input = Tuple[List[bool], Image]


def convolve(image: Image, center: Point) -> int:
    (ambient, grid) = image
    bits = ""
    (r, c) = center
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if grid.get((r + dr, c + dc), ambient):
                bits += "1"
            else:
                bits += "0"
    return int(bits, base=2)


def test_convolve() -> None:
    (_, image) = parse_input(TEST_INPUT)
    assert convolve(image, (2, 2)) == 34


def enhance(image: Image, enhancement: List[bool]) -> Image:
    new_grid = {}
    (ambient, grid) = image
    least_r = min(r for (r, c) in grid.keys())
    greatest_r = max(r for (r, c) in grid.keys())
    least_c = min(c for (r, c) in grid.keys())
    greatest_c = max(c for (r, c) in grid.keys())
    for r in range(least_r - 1, greatest_r + 2):
        for c in range(least_c - 1, greatest_c + 2):
            new_grid[r, c] = enhancement[convolve(image, (r, c))]

    if ambient:
        ambient = enhancement[-1]
    else:
        ambient = enhancement[0]
    return (ambient, new_grid)


def print_image(image: Image) -> None:
    (_ambient, grid) = image
    least_r = min(r for (r, c) in grid.keys())
    greatest_r = max(r for (r, c) in grid.keys())
    least_c = min(c for (r, c) in grid.keys())
    greatest_c = max(c for (r, c) in grid.keys())
    for r in range(least_r, greatest_r + 1):
        for c in range(least_c, greatest_c + 1):
            sys.stdout.write("#" if grid[r, c] else ".")
        sys.stdout.write("\n")


def part1(input: Input) -> str:
    (enhancement, image) = input
    image = enhance(image, enhancement)
    print_image(image)
    image = enhance(image, enhancement)
    assert image[0] is False
    return str(len([x for x in image[1].values() if x]))


def part2(input: Input) -> str:
    (enhancement, image) = input
    for i in range(50):
        image = enhance(image, enhancement)
    assert image[0] is False
    return str(len([x for x in image[1].values() if x]))


def parse_input(input: str) -> Input:
    (enhancement_str, image_str) = input.strip().split("\n\n")
    enhancement = [bool(x == "#") for x in enhancement_str]
    assert len(enhancement) == 512
    image = {}
    for (r, line) in enumerate(image_str.splitlines()):
        for (c, char) in enumerate(line):
            image[r, c] = char == "#"
    return (enhancement, (False, image))


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
