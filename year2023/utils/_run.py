import inspect
import logging
import re
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

TInput = TypeVar("TInput")

_DAY_RE = re.compile(r"day(\d+)")
_YEAR_RE = re.compile(r"year(\d+)")


class Solution(Generic[TInput], ABC):
    @abstractmethod
    def parse_input(self, input: str) -> TInput:
        raise NotImplementedError()

    @abstractmethod
    def part1(self, input: TInput) -> object:
        raise NotImplementedError()

    @abstractmethod
    def part2(self, input: TInput) -> object:
        raise NotImplementedError()

    def _class_def_path(self) -> Path:
        return Path(inspect.getfile(self.__class__))

    def year(self) -> int:
        dir = self._class_def_path().parent.parent.name
        match = _YEAR_RE.match(dir)
        assert match is not None, f"Could not extract year from directory {dir!r}"
        return int(match.group(1))

    def day(self) -> int:
        dir = self._class_def_path().parent.name
        match = _DAY_RE.match(dir)
        assert match is not None, f"Could not extract day from directory {dir!r}"
        return int(match.group(1))

    def main(self) -> None:
        # https://stackoverflow.com/a/44175370/344643
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        input_path = self._class_def_path().parent / "input"
        if not input_path.exists():
            logging.info("Downloading input...")
            try:
                subprocess.check_call(
                    [
                        "aoc",
                        "download",
                        "--input-only",
                        "--year",
                        str(self.year()),
                        "--day",
                        str(self.day()),
                        "--input-file",
                        str(input_path),
                    ]
                )
            except FileNotFoundError as e:
                raise RuntimeError(
                    "Could not download input. (Does the `aoc` binary exist? Install with `cargo install aoc-cli`.)"
                ) from e
        input_str = input_path.read_text()
        input = self.parse_input(input_str)

        print("part 1:", self.part1(input))
        print("part 2:", self.part2(input))
