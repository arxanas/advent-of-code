import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

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


def part1(input: Input) -> int:
    result = 0
    for line in input:
        midpoint = len(line) // 2
        lhs = line[:midpoint]
        rhs = line[midpoint:]
        common = list(set(lhs) & set(rhs))[0]
        assert len(common) == 1
        if "a" <= common <= "z":
            result += ord(common) - ord("a") + 1
        elif "A" <= common <= "Z":
            result += ord(common) - ord("A") + 1 + 26
        else:
            raise ValueError(common)
    return result


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == 157


def part2(input: Input) -> int:
    result = 0
    groups = []
    for i in range(0, len(input), 3):
        groups.append(input[i : i + 3])
    for (r1, r2, r3) in groups:
        common = list(set(r1) & set(r2) & set(r3))[0]
        assert len(common) == 1
        if "a" <= common <= "z":
            result += ord(common) - ord("a") + 1
        elif "A" <= common <= "Z":
            result += ord(common) - ord("A") + 1 + 26
        else:
            raise ValueError(common)
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
