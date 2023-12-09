import logging
import re


def split_line_groups(input: str) -> list[str]:
    """Split the input into groups of lines separated by blank lines."""
    return input.strip().split("\n\n")


def extract_int_list(input: str) -> list[int]:
    """Extract a list of integers from a string. Non-integral characters are
    used to distinguish between integer boundaries and are otherwise ignored.
    """
    int_re = re.compile(
        r"""
        (
            ((?<!\d)[-+])? # optional sign, only if there wasn't a digit before it, like in 12-34
            \d+
        )
    """,
        flags=re.VERBOSE,
    )
    return [int(x.group(0)) for x in int_re.finditer(input)]


def test_extract_int_list() -> None:
    assert extract_int_list("1 2 3") == [1, 2, 3]
    assert extract_int_list("1-2 3") == [1, 2, 3]
    assert extract_int_list("1 -2 3") == [1, -2, 3]
    assert extract_int_list("foo: 1-2 bar: 3-4") == [1, 2, 3, 4]


def extract_int_list_pairs(input: str) -> list[tuple[int, int]]:
    """Call `extract_list` and group adjacent pairs of integers into tuples."""
    ints = extract_int_list(input)
    if len(ints) % 2 != 0:
        logging.warn(
            "Input list to %s has odd length (%d), ignoring last element",
            extract_int_list_pairs.__name__,
            input,
        )
    return list(zip(ints[::2], ints[1::2]))


def test_extract_int_list_pairs() -> None:
    assert extract_int_list_pairs("1 2") == [(1, 2)]
    assert extract_int_list_pairs("1 2 3 4") == [(1, 2), (3, 4)]
    assert extract_int_list_pairs("ranges: 1-2 3-4") == [(1, 2), (3, 4)]
