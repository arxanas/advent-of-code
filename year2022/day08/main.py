from functools import reduce
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import utils

TEST_INPUT = """
30373
25512
65332
33549
35390
"""

PART_1_ANSWER = 21
PART_2_ANSWER = 8

Input = list[list[int]]


def parse_input(input: str) -> Input:
    rows = []
    for line in input.strip().splitlines():
        row = []
        for char in line:
            row.append(int(char))
        rows.append(row)
    return rows


def is_visible_from_edge(input: Input, start_ij: tuple[int, int]) -> bool:
    size = len(input)
    (i, j) = start_ij
    cell = input[i][j]
    for other_i in range(0, i):
        if input[other_i][j] >= cell:
            break
    else:
        return True

    for other_i in range(i + 1, size):
        if input[other_i][j] >= cell:
            break
    else:
        return True

    for other_j in range(0, j):
        if input[i][other_j] >= cell:
            break
    else:
        return True

    for other_j in range(j + 1, size):
        if input[i][other_j] >= cell:
            break
    else:
        return True

    return False


def part1(input: Input) -> int:
    size = len(input)
    result = 0
    for (i, row) in enumerate(input):
        for (j, _cell) in enumerate(row):
            if is_visible_from_edge(input, (i, j)):
                result += 1
    return result


def calc_scenic_score(input: Input, ij: tuple[int, int]) -> int:
    size = len(input)
    (i, j) = ij
    cell = input[i][j]
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    scores = []
    for (di, dj) in deltas:
        delta_score = 0
        k = i + di
        l = j + dj
        while 0 <= k < size and 0 <= l < size:
            delta_score += 1
            if input[k][l] >= cell:
                break
            k += di
            l += dj
        scores.append(delta_score)
    return reduce(lambda x, y: x * y, scores, 1)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    size = len(input)
    return max(
        calc_scenic_score(input, (i, j)) for i in range(size) for j in range(size)
    )


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
