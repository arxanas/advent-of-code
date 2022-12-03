from typing import Iterable, Optional, Sequence, TypeVar, cast

import pytest

T = TypeVar("T")


def split_line_groups(input: str) -> list[str]:
    """Split the input into groups of lines separated by blank lines."""
    return input.strip().split("\n\n")


def split_into_groups_of_size_n(input: Sequence[T], n: int) -> list[Sequence[T]]:
    """Split the input into groups of n values. If there aren't enough values to
    fill the last group, it will be have fewer than n values.
    """
    return [input[i : i + n] for i in range(0, len(input), n)]


def test_split_into_groups_of_size_n() -> None:
    assert split_into_groups_of_size_n("foobar", 2) == ["fo", "ob", "ar"]
    assert split_into_groups_of_size_n("foobar", 3) == ["foo", "bar"]


def split_into_n_groups_exn(input: Sequence[T], n: int) -> list[Sequence[T]]:
    """Split the input into n groups of equal size. If there aren't enough values
    to fill the last group, an exception will be raised.
    """
    remainder = len(input) % n
    if remainder != 0:
        raise ValueError(
            "Input sequence has length {}, which is not divisible by {} (remainder: {}): {!r}".format(
                len(input),
                n,
                remainder,
                input,
            )
        )
    group_size = len(input) // n
    return [input[i : i + group_size] for i in range(0, len(input), group_size)]


def test_split_into_n_groups_exn() -> None:
    assert split_into_n_groups_exn("foobar", 2) == ["foo", "bar"]
    assert split_into_n_groups_exn("foobar", 3) == ["fo", "ob", "ar"]
    with pytest.raises(ValueError):
        split_into_n_groups_exn("foobar", 4)


def only(seq: Iterable[T]) -> Optional[T]:
    """Return the only element of the iterable, or return None if the iterable
    is empty or has more than one element."""
    seen_elem = False
    to_return = None
    for elem in seq:
        if seen_elem:
            return None
        to_return = elem
        seen_elem = True
    if not seen_elem:
        return None
    return to_return


def test_only() -> None:
    assert only([1]) == 1
    assert only([1, 2]) is None
    assert only([]) is None


def only_exn(seq: Iterable[T]) -> T:
    """Return the only element of the iterable, or raise an exception if the
    iterable is empty or has more than one element."""
    seen_elem = False
    to_return = None
    for elem in seq:
        if seen_elem:
            raise ValueError(
                "Expected only one element, but got more: {!r}".format(seq)
            )
        to_return = elem
        seen_elem = True
    if not seen_elem:
        raise ValueError("Iterable is empty")
    return cast(T, to_return)


def test_only_exn() -> None:
    assert only_exn([1]) == 1
    with pytest.raises(ValueError, match="Expected only one element"):
        only_exn([1, 2])
    with pytest.raises(ValueError, match="Iterable is empty"):
        only_exn([])
