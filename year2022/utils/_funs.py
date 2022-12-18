import functools
import itertools
import operator
from typing import Callable, Iterable, Optional, Sequence, TypeVar, cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

T = TypeVar("T")


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


def assert_in_bounds(container: Sequence[object], index: int) -> int:
    """Assert that the given index is in bounds for the given container."""
    assert (
        0 <= index < len(container)
    ), f"Index {index} is out of bounds for container of length {len(container)}"
    return index


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


def maybe_strip_prefix(s: str, prefix: str) -> Optional[str]:
    """Return s with the given prefix removed if it's present, otherwise return
    None.
    """
    if s.startswith(prefix):
        return s[len(prefix) :]
    else:
        return None


def test_maybe_strip_prefix() -> None:
    assert maybe_strip_prefix("foobar", "foo") == "bar"
    assert maybe_strip_prefix("foobar", "bar") is None


def count(iterable: Iterable[T]) -> int:  # type: ignore
    """Return the number of elements in the given iterable."""
    return sum(1 for _ in iterable)


def test_count() -> None:
    assert count([0, 1, 2, 3, 4]) == 5


iota = itertools.count


def test_iota() -> None:
    assert list(itertools.islice(iota(), 5)) == [0, 1, 2, 3, 4]


def take_while(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Iterable[T]:
    """Return elements from the given iterable as long as the given predicate
    returns True.
    """
    # Reimplementing this because itertools.takewhile() doesn't seem to be
    # generic.
    return itertools.takewhile(predicate, iterable)


def test_take_while() -> None:
    assert list(take_while(lambda x: x < 3, [0, 1, 2, 3, 4])) == [0, 1, 2]


def unique_ordered(iterable: Iterable[T]) -> Iterable[T]:
    """Return a list of the unique elements in the given iterable, in the order
    they first appeared.
    """
    seen: set[T] = set()
    for elem in iterable:
        if elem not in seen:
            seen.add(elem)
            yield elem


def test_unique_ordered() -> None:
    assert list(unique_ordered([1, 2, 3, 2, 1])) == [1, 2, 3]


def product_int(iterable: Iterable[int]) -> int:
    """Return the numeric product of the elements in the given iterable."""
    return functools.reduce(operator.mul, iterable, 1)


def test_product_int() -> None:
    assert product_int([]) == 1
    assert product_int([1, 2, 3, 4]) == 24


def product_float(iterable: Iterable[float]) -> float:
    """Return the numeric product of the elements in the given iterable."""
    return functools.reduce(operator.mul, iterable, 1.0)


def test_product_float() -> None:
    assert product_int([]) == 1.0
    assert product_float([1.0, 2.0, 3.0, 4.0]) == 24.0


def clamp_int(value: int, min_value: int, max_value: int) -> int:
    """Return the given value, clamped to the given range."""
    return max(min(value, max_value), min_value)


def split(
    iterable: Iterable[T], predicate: Callable[[T], bool]
) -> Iterable[Iterable[T]]:
    """Split the given iterable into sub-iterables whenever the given predicate
    returns True.
    """
    current: list[T] = []
    for elem in iterable:
        if predicate(elem):
            yield current
            current = []
        else:
            current.append(elem)
    if current:
        yield current


def test_split() -> None:
    assert list(split([1, 2, 3, 4, 5], lambda x: x == 3)) == [[1, 2], [4, 5]]
    assert list(split([1, 2, 3, 4, 5], lambda x: x == 6)) == [[1, 2, 3, 4, 5]]
    assert list(split([1, 2, 3, 4, 5], lambda x: x % 2 == 0)) == [[1], [3], [5]]


def find(
    iterable: Iterable[T], predicate: Callable[[T], bool]
) -> Optional[tuple[int, T]]:
    """Return the first element in the given iterable for which the given
    predicate returns True, along with its index. If no such element is found,
    return None.
    """
    for i, elem in enumerate(iterable):
        if predicate(elem):
            return (i, elem)
    return None


def test_find() -> None:
    assert find([1, 2, 3, 4, 5], lambda x: x == 3) == (2, 3)
    assert find([1, 2, 3, 4, 5], lambda x: x == 6) is None


def floyd_warshall(adjacency: dict[T, dict[T, int]]) -> dict[tuple[T, T], int]:
    # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
    distances: dict[tuple[T, T], int] = {}
    for node, neighbors in adjacency.items():
        distances[node, node] = 0
        for (neighbor, distance) in neighbors.items():
            distances[node, neighbor] = distance

    for k in adjacency:
        for i in adjacency:
            for j in adjacency:
                ik = distances.get((i, k))
                if ik is None:
                    continue
                kj = distances.get((k, j))
                if kj is None:
                    continue
                ij = distances.get((i, j))
                if ij is None:
                    distances[i, j] = ik + kj
                else:
                    distances[i, j] = min(ij, ik + kj)
    return distances


def test_floyd_warshall() -> None:
    adjacency = {
        "A": {"B": 1, "C": 5},
        "B": {"C": 2},
        "C": {"D": 1},
        "D": {"B": 1},
    }
    distances = floyd_warshall(adjacency)
    assert distances == {
        ("A", "A"): 0,
        ("A", "B"): 1,
        ("A", "C"): 3,
        ("A", "D"): 4,
        ("B", "B"): 0,
        ("B", "C"): 2,
        ("B", "D"): 3,
        ("C", "B"): 2,
        ("C", "C"): 0,
        ("C", "D"): 1,
        ("D", "B"): 1,
        ("D", "C"): 3,
        ("D", "D"): 0,
    }
