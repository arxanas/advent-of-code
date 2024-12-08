from __future__ import annotations

import sys
from dataclasses import dataclass

from .. import utils

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
    executable: str
    output: list[list[str]]


@dataclass
class Filesystem:
    seen_dirs: set[str]
    seen_files: dict[str, int]

    def calculate_dir_size(self, dir: str) -> int:
        return sum(
            size
            for filename, size in self.seen_files.items()
            if filename.startswith(dir + "/")
        )

    @classmethod
    def from_commands(cls, commands: list[Command]) -> "Filesystem":
        # Note that the root directory is represented by the empty string,
        # rather than "/".
        current_dir: list[str] = []
        seen_dirs: set[str] = set([])
        seen_files: dict[str, int] = {}

        for command in commands:
            maybe_filename = utils.maybe_strip_prefix(command.executable, prefix="cd ")
            if maybe_filename is not None:
                if maybe_filename == "..":
                    current_dir.pop()
                else:
                    current_dir.append(maybe_filename)
                seen_dirs.add("/".join(current_dir))
            elif command.executable == "ls":
                for line in command.output:
                    (lhs, rhs) = line
                    filename = "/".join(current_dir + [rhs])
                    if lhs == "dir":
                        seen_dirs.add(filename)
                    else:
                        seen_files[filename] = int(lhs)
            else:
                raise ValueError("Unknown command: " + command.executable)

        return cls(seen_dirs=seen_dirs, seen_files=seen_files)


Input = list[Command]


def parse_input(input: str) -> Input:
    result = []
    for line in input.strip().splitlines():
        maybe_executable = utils.maybe_strip_prefix(line, prefix="$ ")
        if maybe_executable is not None:
            result.append(Command(executable=maybe_executable, output=[]))
        else:
            result[-1].output.append(line.split(" "))
    return result


def part1(input: Input) -> int:
    filesystem = Filesystem.from_commands(input)
    return sum(
        dir_size
        for dir in filesystem.seen_dirs
        if (dir_size := filesystem.calculate_dir_size(dir)) < 100_000
    )


def test_part1() -> None:
    assert part1(parse_input(TEST_INPUT)) == PART_1_ANSWER


def part2(input: Input) -> int:
    filesystem = Filesystem.from_commands(input)

    total_space = 70_000_000
    used_space = filesystem.calculate_dir_size("")
    unused_space = total_space - used_space
    required_space = 30_000_000
    required_dir_size = required_space - unused_space
    return min(
        size
        for dir in filesystem.seen_dirs
        if (size := filesystem.calculate_dir_size(dir)) >= required_dir_size
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
