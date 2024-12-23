from __future__ import annotations

import logging
import re
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def split_lines(input: str) -> list[str]:
    r"""Strip whitespace and split the input into lines.

    >>> split_lines("\n\nfoo\nbar\nbaz\n\n")
    ['foo', 'bar', 'baz']
    """
    return input.strip().splitlines()


def split_line_groups(input: str) -> list[str]:
    """Split the input into groups of lines separated by blank lines.

    >>> split_line_groups("foo\\n\\nbar\\n\\nbaz")
    ['foo', 'bar', 'baz']
    """
    return input.strip().split("\n\n")


def extract_int_list(input: str) -> list[int]:
    """Extract a list of integers from a string. Non-integral characters are
    used to distinguish between integer boundaries and are otherwise ignored.

    >>> extract_int_list("1 2 3")
    [1, 2, 3]
    >>> extract_int_list("1-2 3")
    [1, 2, 3]
    >>> extract_int_list("1 -2 3")
    [1, -2, 3]
    >>> extract_int_list("foo: 1-2 bar: 3-4")
    [1, 2, 3, 4]
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


def extract_int_list_pairs(input: str) -> list[tuple[int, int]]:
    """Call `extract_list` and group adjacent pairs of integers into tuples.

    >>> extract_int_list_pairs("1 2")
    [(1, 2)]
    >>> extract_int_list_pairs("1 2 3")
    [(1, 2)]
    >>> extract_int_list_pairs("1 2 3 4")
    [(1, 2), (3, 4)]
    >>> extract_int_list_pairs("ranges: 1-2 3-4")
    [(1, 2), (3, 4)]
    """
    ints = extract_int_list(input)
    if len(ints) % 2 != 0:
        logging.warning(
            "Input list to %s has odd length (%d), ignoring last element",
            extract_int_list_pairs.__name__,
            len(ints),
        )
    return list(zip(ints[::2], ints[1::2]))


def hex_to_dec(hex: str) -> int:
    """Convert a hexadecimal string to an integer.

    >>> hex_to_dec("ff")
    255
    """
    return int(hex, 16)


def tuple2(value: Iterable[T]) -> tuple[T, T]:
    """Convert an iterable to a tuple of length 2 (statically-typed).

    >>> tuple2([1, 2])
    (1, 2)
    >>> import pytest
    >>> with pytest.raises(ValueError):
    ...     tuple2([1, 2, 3])
    """
    (v1, v2) = tuple(value)
    return (v1, v2)


def tuple3(value: Iterable[T]) -> tuple[T, T, T]:
    """Convert an iterable to a tuple of length 3 (statically-typed).

    >>> tuple3([1, 2, 3])
    (1, 2, 3)
    >>> import pytest
    >>> with pytest.raises(ValueError):
    ...     tuple3([1, 2])
    """
    (v1, v2, v3) = tuple(value)
    return (v1, v2, v3)
