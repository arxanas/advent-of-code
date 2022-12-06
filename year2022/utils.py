from typing import Iterable, Optional, Sequence, TypeVar, cast

from hypothesis import example, given, strategies as st
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


class InclusiveInterval:
    def __init__(self, start: int, end: int) -> None:
        if end < start:
            start, end = end, start
        self.start = start
        self.end = end

    @classmethod
    def from_tuple(cls, value: tuple[int, int]) -> "InclusiveInterval":
        (start, end) = value
        return cls(start=start, end=end)

    def __contains__(self, item) -> bool:
        if isinstance(item, int):
            return self.start <= item <= self.end
        elif isinstance(item, type(self)):
            return (self.start <= item.start <= self.end) and (
                self.start <= item.end <= self.end
            )
        else:
            raise NotImplementedError("Not implemented for type {}".format(type(item)))

    def overlaps(self, other: "InclusiveInterval") -> bool:
        if self.start <= other.start <= self.end:
            return True
        elif other.start <= self.start <= other.end:
            return True
        else:
            return False


@given(st.integers(), st.integers(), st.integers(), st.integers())
def test_inclusive_interval(lhs1: int, lhs2: int, rhs1: int, rhs2: int) -> None:
    lhs = InclusiveInterval(start=lhs1, end=lhs2)
    rhs = InclusiveInterval(start=rhs1, end=rhs2)
    assert lhs in lhs
    assert lhs.overlaps(lhs)
    if lhs.overlaps(rhs):
        assert rhs.overlaps(lhs)
    if lhs in rhs:
        assert lhs.overlaps(rhs)


def assert_in_bounds(container: Sequence[object], index: int) -> None:
    """Assert that the given index is in bounds for the given container."""
    assert (
        0 <= index < len(container)
    ), f"Index {index} is out of bounds for container of length {len(container)}"


def all_different(elements: Iterable[object]) -> bool:
    """Return True if all elements in the iterable are different, including if
    the iterable is empty.
    """
    seen = set()
    for elem in elements:
        if elem in seen:
            return False
        seen.add(elem)
    return True


def test_all_different() -> None:
    assert all_different([1, 2, 3])
    assert not all_different([1, 2, 2])


def all_same(elements: Iterable[object]) -> bool:
    """Return True if all elements are the same, including if the iterable is
    empty."""
    is_first = True
    value = None
    for elem in elements:
        if is_first:
            value = elem
            is_first = False
        else:
            if elem != value:
                return False
    return True


def test_all_same() -> None:
    assert all_same([1, 1, 1])
    assert not all_same([1, 2, 1])


def transpose_lines(lines: Sequence[str]) -> list[str]:
    """Transpose the given lines of text, so that the first line becomes the
    first column, the second line becomes the second column, etc. Lines are
    first padded with the space character " " so that they are all the same
    length.
    """
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]
    return ["".join(line[i] for line in lines) for i in range(max_len)]


def test_transpose_lines() -> None:
    assert transpose_lines(["abc", "def", "ghi"]) == ["adg", "beh", "cfi"]
    assert transpose_lines(["abc", "defg", "hi"]) == ["adh", "bei", "cf ", " g "]
