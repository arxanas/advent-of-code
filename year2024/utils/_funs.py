import builtins
import functools
import itertools
import operator
from typing import (
    Callable,
    Iterable,
    Optional,
    Sequence,
    TypeVar,
    cast,
)

from hypothesis import given
from hypothesis import strategies as st

T = TypeVar("T")


def split_into_groups_of_size_n(input: Sequence[T], n: int) -> list[Sequence[T]]:
    """Split the input into groups of n values. If there aren't enough values to
    fill the last group, it will be have fewer than n values.

    >>> split_into_groups_of_size_n("foobar", 2)
    ['fo', 'ob', 'ar']
    >>> split_into_groups_of_size_n("foobar", 3)
    ['foo', 'bar']
    """
    return [input[i : i + n] for i in range(0, len(input), n)]


def split_into_n_groups_exn(input: Sequence[T], n: int) -> list[Sequence[T]]:
    """Split the input into n groups of equal size. If there aren't enough values
    to fill the last group, an exception will be raised.

    >>> split_into_n_groups_exn("foobar", 2)
    ['foo', 'bar']
    >>> split_into_n_groups_exn("foobar", 3)
    ['fo', 'ob', 'ar']
    >>> import pytest
    >>> with pytest.raises(ValueError):
    ...     split_into_n_groups_exn("foobar", 4)
    """
    remainder = len(input) % n
    if remainder != 0:
        raise ValueError(
            f"Input sequence has length {len(input)}, which is not divisible by {n} (remainder: {remainder}): {input!r}"
        )
    group_size = len(input) // n
    return [input[i : i + group_size] for i in range(0, len(input), group_size)]


def only(seq: Iterable[T]) -> Optional[T]:
    """Return the only element of the iterable, or return None if the iterable
        is empty or has more than one element.

    >>> only([1])
    1
    >>> repr(only([1, 2]))
    'None'
    >>> repr(only([]))
    'None'
    """
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


def only_exn(seq: Iterable[T]) -> T:
    """Return the only element of the iterable, or raise an exception if the
    iterable is empty or has more than one element.

    >>> only_exn([1])
    1
    >>> import pytest
    >>> with pytest.raises(ValueError, match="Iterable is empty"):
    ...     only_exn([])
    >>> with pytest.raises(ValueError, match="Expected only one element"):
    ...     only_exn([1, 2])
    """
    seen_elem = False
    to_return = None
    for elem in seq:
        if seen_elem:
            raise ValueError(
                "Expected only one element, but got more: {!r}, {!r}, ... in sequence {!r}".format(
                    to_return, elem, seq
                )
            )
        to_return = elem
        seen_elem = True
    if not seen_elem:
        raise ValueError("Iterable is empty")
    return cast(T, to_return)


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
        """Determine if this interval overlaps with the other interval.

        >>> InclusiveInterval(1, 3).overlaps(InclusiveInterval(2, 4))
        True
        >>> InclusiveInterval(1, 3).overlaps(InclusiveInterval(3, 4))
        True
        >>> InclusiveInterval(1, 3).overlaps(InclusiveInterval(4, 5))
        False
        """
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
    """Assert that the given index is in bounds for the given container.

    >>> assert_in_bounds([1, 2, 3], 1)
    1
    >>> import pytest
    >>> with pytest.raises(AssertionError):
    ...     assert_in_bounds([1, 2, 3], 3)
    """
    assert (
        0 <= index < len(container)
    ), f"Index {index} is out of bounds for container of length {len(container)}"
    return index


def all_different(elements: Iterable[object]) -> bool:
    """Return True if all elements in the iterable are different, including if
    the iterable is empty.

    >>> all_different([1, 2, 3])
    True
    >>> all_different([1, 2, 2])
    False
    >>> all_different([])
    True
    >>> all_different([1])
    True
    """
    seen = set()
    for elem in elements:
        if elem in seen:
            return False
        seen.add(elem)
    return True


def all_same(elements: Iterable[object]) -> bool:
    """Return True if all elements are the same, including if the iterable is
    empty.

    >>> all_same([1, 1, 1])
    True
    >>> all_same([1, 2, 1])
    False
    >>> all_same([])
    True
    >>> all_same([1])
    True
    """
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

    >>> transpose_lines(["abc", "def", "ghi"])
    ['adg', 'beh', 'cfi']
    >>> transpose_lines(["abc", "defg", "hi"])
    ['adh', 'bei', 'cf ', ' g ']
    """
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]
    return ["".join(line[i] for line in lines) for i in range(max_len)]


def maybe_strip_prefix(s: str, prefix: str) -> Optional[str]:
    """Return s with the given prefix removed if it's present, otherwise return
    None.

    >>> maybe_strip_prefix("foobar", "foo")
    'bar'
    >>> repr(maybe_strip_prefix("foobar", "bar"))
    'None'
    """
    if s.startswith(prefix):
        return s[len(prefix) :]
    else:
        return None


def count(iterable: Iterable[T]) -> int:  # type: ignore
    """Return the number of elements in the given iterable.

    >>> count([0, 1, 2, 3, 4])
    5
    """
    return sum(1 for _ in iterable)


def iota() -> Iterable[int]:
    """Return an infinite iterable of integers starting from 0.

    >>> list(itertools.islice(iota(), 5))
    [0, 1, 2, 3, 4]
    """
    return itertools.count()


def take_while(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Iterable[T]:
    """Return elements from the given iterable as long as the given predicate
    returns True.


    >>> list(take_while(lambda x: x < 3, [0, 1, 2, 3, 4]))
    [0, 1, 2]
    """
    # Reimplementing this because itertools.takewhile() doesn't seem to be
    # generic.
    return itertools.takewhile(predicate, iterable)


def unique_ordered(iterable: Iterable[T]) -> Iterable[T]:
    """Return an iterable of the unique elements in the given iterable, in the
    order they first appeared.

    >>> list(unique_ordered([1, 2, 3, 2, 1]))
    [1, 2, 3]
    """
    seen: set[T] = set()
    for elem in iterable:
        if elem not in seen:
            seen.add(elem)
            yield elem


def product_int(iterable: Iterable[int]) -> int:
    """Return the numeric product of the elements in the given iterable.

    >>> product_int([1, 2, 3, 4])
    24
    >>> product_int([])
    1
    """
    return functools.reduce(operator.mul, iterable, 1)


def product_float(iterable: Iterable[float]) -> float:
    """Return the numeric product of the elements in the given iterable.

    >>> product_float([1.0, 2.0, 3.0, 4.0])
    24.0
    >>> product_float([])
    1.0
    """
    return functools.reduce(operator.mul, iterable, 1.0)


def clamp_int(value: int, min: int, max: int) -> int:
    """Return the given value, clamped to the given range.

    >>> clamp_int(5, min=0, max=10)
    5
    >>> clamp_int(-5, 0, 10)
    0
    >>> clamp_int(15, 0, 10)
    10
    """
    return builtins.max(builtins.min(value, max), min)


def split(
    iterable: Iterable[T], predicate: Callable[[T], bool]
) -> Iterable[Iterable[T]]:
    """Split the given iterable into sub-iterables whenever the given predicate
    returns True.

    >>> list(split([1, 2, 3, 4, 5], lambda x: x == 3))
    [[1, 2], [4, 5]]
    >>> list(split([1, 2, 3, 4, 5], lambda x: x == 6))
    [[1, 2, 3, 4, 5]]
    >>> list(split([1, 2, 3, 4, 5], lambda x: x % 2 == 0))
    [[1], [3], [5]]
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


def find(
    iterable: Iterable[T], predicate: Callable[[T], bool]
) -> Optional[tuple[int, T]]:
    """Return the first element in the given iterable for which the given
    predicate returns True, along with its index. If no such element is found,
    return None.

    >>> find([1, 2, 3, 4, 5], lambda x: x == 3)
    (2, 3)
    >>> find([1, 2, 3, 4, 5], lambda x: x == 6) is None
    True
    """
    for i, elem in enumerate(iterable):
        if predicate(elem):
            return (i, elem)
    return None


def floyd_warshall(adjacency: dict[T, dict[T, int]]) -> dict[tuple[T, T], int]:
    """Calculate the shortest distances between all pairs of nodes in the given
    graph, using the [Floyd-Warshall algorithm][floyd-warshall], in O(n^3) time.

      [floyd-warshall]: https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm

    >>> adjacency = {
    ...     "A": {"B": 1, "C": 5},
    ...     "B": {"C": 2},
    ...     "C": {"D": 1},
    ...     "D": {"B": 1},
    ... }
    >>> import pprint
    >>> pprint.pprint(floyd_warshall(adjacency))
    {('A', 'A'): 0,
     ('A', 'B'): 1,
     ('A', 'C'): 3,
     ('A', 'D'): 4,
     ('B', 'B'): 0,
     ('B', 'C'): 2,
     ('B', 'D'): 3,
     ('C', 'B'): 2,
     ('C', 'C'): 0,
     ('C', 'D'): 1,
     ('D', 'B'): 1,
     ('D', 'C'): 3,
     ('D', 'D'): 0}
    """
    distances: dict[tuple[T, T], int] = {}
    for node, neighbors in adjacency.items():
        distances[node, node] = 0
        for neighbor, distance in neighbors.items():
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


def find_subsequence(input: Sequence[T], subsequence: Sequence[T]) -> Optional[int]:
    """
    >>> find_subsequence([], [])
    0
    >>> repr(find_subsequence([], [1]))
    'None'
    >>> find_subsequence([1], [])
    0
    >>> find_subsequence([1], [1])
    0
    >>> find_subsequence([1, 2], [1])
    0
    >>> find_subsequence([1, 2], [2])
    1
    >>> find_subsequence([1, 2], [1, 2])
    0
    >>> repr(find_subsequence([1, 2], [2, 1]))
    'None'
    >>> find_subsequence([1, 2, 3], [1, 2])
    0
    >>> find_subsequence([1, 2, 3], [2, 3])
    1
    >>> repr(find_subsequence([1, 2, 3], [3, 1]))
    'None'
    """
    for i in range(len(input) - len(subsequence) + 1):
        if input[i : i + len(subsequence)] == subsequence:
            return i
    return None


def minmax(iterable: Iterable[T]) -> tuple[T, T]:
    """Return the minimum and maximum elements in the given iterable.

    >>> minmax([1, 2, 3, 4, 5])
    (1, 5)
    >>> minmax([5, 4, 3, 2, 1])
    (1, 5)
    >>> minmax([1])
    (1, 1)
    >>> import pytest
    >>> with pytest.raises(ValueError):
    ...     minmax([])
    """
    iterator = iter(iterable)
    try:
        first = next(iterator)
    except StopIteration:
        raise ValueError("Iterable is empty")
    min_elem = first
    max_elem = first
    for elem in iterator:
        if elem < min_elem:  # type: ignore[operator]
            min_elem = elem
        if elem > max_elem:  # type: ignore[operator]
            max_elem = elem
    return min_elem, max_elem


def flatten(iterable: Iterable[Iterable[T]]) -> Iterable[T]:
    """Flatten the given iterable of iterables into a single iterable.

    >>> list(flatten([[1, 2], [3, 4], [5, 6]]))
    [1, 2, 3, 4, 5, 6]
    >>> list(flatten([[1, 2], [], [3, 4], [5, 6]]))
    [1, 2, 3, 4, 5, 6]
    >>> list(flatten([]))
    []
    """
    return itertools.chain.from_iterable(iterable)
