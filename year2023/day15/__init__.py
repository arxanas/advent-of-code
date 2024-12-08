from __future__ import annotations

from dataclasses import dataclass

from .. import utils as u

TEST_INPUT1 = r"""
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 1320
PART_2_ANSWER = 145


def test_part1() -> None:
    assert Solution.parse_input(TEST_INPUT1).part1() == PART_1_ANSWER


def test_part2() -> None:
    assert Solution.parse_input(TEST_INPUT2).part2() == PART_2_ANSWER


@dataclass
class Solution(u.Solution):
    input: list[str]
    operations: list[tuple[str, int | None]]

    @classmethod
    def parse_input(cls, input: str) -> "Solution":
        values = input.strip().split(",")
        operations: list[tuple[str, int | None]] = []
        for op in values:
            if op.endswith("-"):
                operations.append((op[:-1], None))
            else:
                (lhs, rhs) = op.split("=")
                operations.append((lhs, int(rhs)))
        return cls(input=values, operations=operations)

    def _hash(self, s: str) -> int:
        value = 0
        for c in s:
            value += ord(c)
            value *= 17
            value %= 256
        return value

    def part1(self) -> int:
        return sum(self._hash(s) for s in self.input)

    def part2(self) -> int:
        @dataclass
        class Lens:
            label: str
            value: int

        boxes: list[list[Lens]] = [[] for _ in range(256)]
        for operation in self.operations:
            (label, value) = operation
            idx = self._hash(label)
            match value:
                case None:
                    boxes[idx] = [lens for lens in boxes[idx] if lens.label != label]
                case int(value):
                    new_lens = Lens(label=label, value=value)
                    if any(lens.label == label for lens in boxes[idx]):
                        boxes[idx] = [
                            new_lens if lens.label == label else lens
                            for lens in boxes[idx]
                        ]
                    else:
                        boxes[idx].append(new_lens)
            assert len(boxes[idx]) < 10

        return sum(
            sum(i * j * lens.value for (j, lens) in enumerate(box, 1))
            for (i, box) in enumerate(boxes, 1)
        )
