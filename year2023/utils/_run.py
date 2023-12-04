import inspect
import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

TInput = TypeVar("TInput")

_DAY_RE = re.compile(r"day(\d+)")
_YEAR_RE = re.compile(r"year(\d+)")


class Solution(Generic[TInput], ABC):
    @property
    @abstractmethod
    def TEST_INPUT1(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def TEST_INPUT2(self) -> str:
        raise NotImplementedError()

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

    def main(self) -> None:
        # https://stackoverflow.com/a/44175370/344643
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        input_path = self._class_def_path().parent / "input"
        input_str = input_path.read_text()
        input = self.parse_input(input_str)

        print("test 1:", self.part1(self.parse_input(self.TEST_INPUT1)))
        print("part 1:", self.part1(input))
        print("test 2:", self.part2(self.parse_input(self.TEST_INPUT2)))
        print("part 2:", self.part2(input))
