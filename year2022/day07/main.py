from dataclasses import dataclass
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import utils

TEST_INPUT = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

PART_1_ANSWER = 95437
PART_2_ANSWER = 24933642


@dataclass
class Command:
    command: str
    output: list[list[str]]


Input = list[Command]


def parse_input(input: str) -> Input:
    result = []
    for line in input.strip().splitlines():
        if line.startswith("$ "):
            result.append(Command(line[2:], []))
        else:
            result[-1].output.append(line.split(" "))
    return result


def part1(input: Input) -> int:
    current_dir = []
    seen_dirs: set[str] = set([])
    seen_files: dict[str, int] = {}
    for command in input:
        if command.command.startswith("cd "):
            filename = command.command[3:]
            if filename == "..":
                current_dir.pop()
            else:
                current_dir.append(filename)
            seen_dirs.add("/".join(current_dir))
        elif command.command == "ls":
            for line in command.output:
                (lhs, rhs) = line
                filename = "/".join(current_dir + [rhs])
                if lhs == "dir":
                    seen_dirs.add(filename)
                else:
                    seen_files[filename] = int(lhs)

    dir_sizes: dict[str, int] = {}

    def calculate_dir_size(dir: str) -> int:
        result = 0
        for filename in seen_files:
            if filename.startswith(dir + "/"):
                result += seen_files[filename]
        return result

    sizes = [x for dir in seen_dirs if (x := calculate_dir_size(dir)) < 100_000]
    return sum(sizes)


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    current_dir = []
    seen_dirs: set[str] = set([])
    seen_files: dict[str, int] = {}
    for command in input:
        if command.command.startswith("cd "):
            filename = command.command[3:]
            if filename == "..":
                current_dir.pop()
            else:
                current_dir.append(filename)
            seen_dirs.add("/".join(current_dir))
        elif command.command == "ls":
            for line in command.output:
                (lhs, rhs) = line
                filename = "/".join(current_dir + [rhs])
                if lhs == "dir":
                    seen_dirs.add(filename)
                else:
                    seen_files[filename] = int(lhs)

    dir_sizes: dict[str, int] = {}

    def calculate_dir_size(dir: str) -> int:
        result = 0
        for filename in seen_files:
            if filename.startswith(dir + "/"):
                result += seen_files[filename]
        return result

    total_space = 70_000_000
    used_space = calculate_dir_size("")
    unused_space = total_space - used_space
    required_space = 30_000_000
    required_dir_size = required_space - unused_space
    sizes = [
        size
        for dir in seen_dirs
        if (size := calculate_dir_size(dir)) >= required_dir_size
    ]
    return min(sizes)


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
