from typing import Optional, Sequence, TypeVar

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


def only(seq: Sequence[T]) -> Optional[T]:
    """Return the only element of the sequence, or None if the sequence is empty
    or has more than one element.
    """
    if len(seq) == 1:
        return seq[0]
    else:
        return None


def test_only() -> None:
    assert only([1]) == 1
    assert only([1, 2]) is None
    assert only([]) is None


def only_exn(seq: Sequence[T]) -> Optional[T]:
    """Return the only element of the sequence, or None if the sequence is empty
    or has more than one element.
    """
    if len(seq) == 1:
        return seq[0]
    else:
        raise ValueError(
            "Expected exactly one element, got {} in sequence {!r}".format(
                len(seq), seq
            )
        )


def test_onlyx() -> None:
    assert only_exn([1]) == 1
    with pytest.raises(ValueError):
        only_exn([1, 2])
    with pytest.raises(ValueError):
        only_exn([])
