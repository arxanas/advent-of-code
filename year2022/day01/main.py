import sys

TEST_INPUT = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

Input = list[list[int]]


def parse_input(input: str) -> Input:
    groups = input.strip().split("\n\n")
    return [
        [int(calories) for calories in group.strip().split("\n")] for group in groups
    ]


def part1(input: Input) -> str:
    max_calories = max(sum(group) for group in input)
    return str(max_calories)


def part2(input: Input) -> str:
    calorie_sums = [sum(group) for group in input]
    calorie_sums.sort(reverse=True)
    return str(sum(calorie_sums[:3]))


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
