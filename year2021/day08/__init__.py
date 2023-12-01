"""
Note: I am not proud of this code.
"""

import sys
from collections import *
from functools import *
from typing import *

TEST_INPUT = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""


def part1(input: List[Tuple[List[str], List[str]]]) -> str:
    count = 0
    for _, outputs in input:
        for output_val in outputs:
            if len(output_val) in [2, 3, 4, 7]:
                count += 1
    return str(count)


NUMBERS = {
    0: [1, 1, 1, 0, 1, 1, 1],
    1: [0, 0, 1, 0, 0, 1, 0],
    2: [1, 0, 1, 1, 1, 0, 1],
    3: [1, 0, 1, 1, 0, 1, 1],
    4: [0, 1, 1, 1, 0, 1, 0],
    5: [1, 1, 0, 1, 0, 1, 1],
    6: [1, 1, 0, 1, 1, 1, 1],
    7: [1, 0, 1, 0, 0, 1, 0],
    8: [1, 1, 1, 1, 1, 1, 1],
    9: [1, 1, 1, 1, 0, 1, 1],
}


def is_consistent(input: List[str], assignment: Dict[str, int]) -> bool:
    for letter, signal in assignment.items():
        for input_val in input:
            if letter not in input_val:
                continue
            for number_signals in NUMBERS.values():
                if len(input_val) == sum(number_signals):
                    if number_signals[signal]:
                        break
            else:
                return False
    return True


def test_is_consistent() -> None:
    input = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab".split(" ")
    assert is_consistent(
        input,
        {
            "d": 0,
            "e": 1,
            "a": 2,
            "f": 3,
            "g": 4,
            "b": 5,
            "c": 6,
        },
    )
    assert not is_consistent(
        input,
        {
            "d": 0,
            "e": 1,
            "a": 2,
            "f": 6,
            "g": 4,
            "b": 5,
            "c": 3,
        },
    )


def search(input: List[str], assignments: Dict[str, int]) -> Optional[Dict[str, int]]:
    if not is_consistent(input, assignments):
        return None
    if len(assignments) == 7:
        for input_val in input:
            try:
                decode_digit(assignments, input_val)
            except Exception:
                return None
        return assignments

    letter = None
    for next_letter in "abcdefg":
        if next_letter not in assignments:
            letter = next_letter
            break
    assert letter is not None

    for signal in range(0, 7):
        # Don't reuse the same key-value mapping.
        if signal in assignments.values():
            continue

        assignments[letter] = signal
        result = search(input, assignments)
        if result is not None:
            return result
        del assignments[letter]
    return None


def decode_digit(assignment: Dict[str, int], signals: str) -> int:
    bits = [0] * len("abcdefg")
    for char in "abcdefg":
        if char in signals:
            bits[assignment[char]] = 1
    for number, number_signals in NUMBERS.items():
        if number_signals == bits:
            return number
    raise ValueError(
        f"no match for signals {signals!r}, bits {bits!r} in assignment {assignment!r}"
    )


def test_decode_digit() -> None:
    assert decode_digit({"a": 0, "b": 2, "c": 5, "d": 4}, "acb") == 7
    assert (
        decode_digit(
            {
                "d": 0,
                "e": 1,
                "a": 2,
                "f": 3,
                "g": 4,
                "b": 5,
                "c": 6,
            },
            "cdfeb",
        )
        == 5
    )
    assert (
        decode_digit(
            {
                "d": 0,
                "e": 1,
                "a": 2,
                "f": 3,
                "g": 4,
                "b": 5,
                "c": 6,
            },
            "fcadb",
        )
        == 3
    )


def decode(assignment: Dict[str, int], digits: List[str]) -> int:
    return int("".join(str(decode_digit(assignment, signals)) for signals in digits))


def test_decode() -> None:
    assert decode({"a": 0, "b": 2, "c": 5, "d": 4}, ["acb"]) == 7


def part2(input: List[Tuple[List[str], List[str]]]) -> str:
    result = 0
    for input_val, output_val in input:
        assignment = search(input_val + output_val, {})
        print(input_val + output_val)
        print(assignment)
        assert assignment is not None
        result += decode(assignment, output_val)
    return str(result)


def parse_line(input: str) -> Tuple[List[str], List[str]]:
    (a, b) = input.split(" | ")
    return ([i.strip() for i in a.split(" ")], [i.strip() for i in b.split(" ")])


def main() -> None:
    # input = [i for i in sys.stdin.read().strip().split(",")]
    input = [parse_line(i) for i in sys.stdin.read().strip().splitlines()]
    test_input = [parse_line(i) for i in TEST_INPUT.strip().splitlines()]

    print("test 1:", part1(test_input))
    print("test 2:", part2(test_input))
    print("part 1:", part1(input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
