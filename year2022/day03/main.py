import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import split_into_groups_of_size_n, split_into_n_groups_exn

TEST_INPUT = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

Input = list[str]


def parse_input(input: str) -> Input:
    return input.strip().splitlines()


def priority(char: str) -> int:
    assert len(char) == 1
    if "a" <= char <= "z":
        return ord(char) - ord("a") + 1
    elif "A" <= char <= "Z":
        return ord(char) - ord("A") + 1 + 26
    else:
        raise ValueError(char)


def part1(input: Input) -> int:
    result = 0
    for line in input:
        (lhs, rhs) = split_into_n_groups_exn(line, n=2)
        common = list(set(lhs) & set(rhs))[0]
        result += priority(common)
    return result


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == 157


def part2(input: Input) -> int:
    result = 0
    for (r1, r2, r3) in split_into_groups_of_size_n(input, 3):
        common = list(set(r1) & set(r2) & set(r3))[0]
        result += priority(common)
    return result


def test_part2() -> None:
    assert part2(parse_input(TEST_INPUT)) == 70


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
