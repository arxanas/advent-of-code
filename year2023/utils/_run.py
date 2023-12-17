import inspect
import logging
import re
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Self

_DAY_RE = re.compile(r"day(\d+)")
_YEAR_RE = re.compile(r"year(\d+)")


class Solution(ABC):
    @classmethod
    @abstractmethod
    def parse_input(cls, input: str) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def part1(self) -> object:
        raise NotImplementedError()

    @abstractmethod
    def part2(self) -> object:
        raise NotImplementedError()

    @classmethod
    def _class_def_path(cls) -> Path:
        return Path(inspect.getfile(cls))

    @classmethod
    def year(cls) -> int:
        dir = cls._class_def_path().parent.parent.name
        match = _YEAR_RE.match(dir)
        assert match is not None, f"Could not extract year from directory {dir!r}"
        return int(match.group(1))

    @classmethod
    def day(cls) -> int:
        dir = cls._class_def_path().parent.name
        match = _DAY_RE.match(dir)
        assert match is not None, f"Could not extract day from directory {dir!r}"
        return int(match.group(1))

    @classmethod
    def main(cls) -> None:
        # https://stackoverflow.com/a/44175370/344643
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        input_path = cls._class_def_path().parent / "input"
        if not input_path.exists():
            logging.info("Downloading input...")
            try:
                subprocess.check_call(
                    [
                        "aoc",
                        "download",
                        "--input-only",
                        "--year",
                        str(cls.year()),
                        "--day",
                        str(cls.day()),
                        "--input-file",
                        str(input_path),
                    ]
                )
            except FileNotFoundError as e:
                raise RuntimeError(
                    "Could not download input. (Does the `aoc` binary exist? Install with `cargo install aoc-cli`.)"
                ) from e
        input_str = input_path.read_text()
        solution = cls.parse_input(input_str)

        print("part 1:", solution.part1())
        print("part 2:", solution.part2())
