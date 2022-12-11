import functools
import itertools
import operator
from dataclasses import dataclass
from typing import Callable, Generic, Iterable, Optional, Sequence, TypeVar, cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

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


@dataclass(frozen=True, eq=True, order=True)
class Coord:
    """A 3D coordinate, represented as a tuple of (x, y, z).

    For 2D coordinates, z should be 0.
    """

    x: int
    y: int
    z: int

    @classmethod
    def zero(cls) -> "Coord":
        return cls(x=0, y=0, z=0)

    @classmethod
    def from_tuple(cls, value: tuple[int, int, int]) -> "Coord":
        (x, y, z) = value
        return cls(x=x, y=y, z=z)

    @classmethod
    def from_str(cls, value: str) -> "Coord":
        (x, y, z) = value.split(",")
        return cls(x=int(x), y=int(y), z=int(z))

    @classmethod
    def from_2d(cls, x: int, y: int) -> "Coord":
        return cls(x=x, y=y, z=0)

    def to_tuple(self) -> tuple[int, int, int]:
        return (self.x, self.y, self.z)

    def to_2d(self) -> tuple[int, int]:
        assert self.z == 0, "Expected z=0 for 2D coordinate, got z={}".format(self.z)
        return (self.x, self.y)

    def __add__(self, delta: "Delta") -> "Coord":
        return Coord(x=self.x + delta.x, y=self.y + delta.y, z=self.z + delta.z)

    def __sub__(self, other: "Coord") -> "Delta":
        return Delta(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def manhattan_distance(self, other: "Coord") -> int:
        delta = self - other
        return abs(delta.x) + abs(delta.y) + abs(delta.z)

    def chess_distance(self, other: "Coord") -> int:
        delta = self - other
        return max(abs(delta.x), abs(delta.y), abs(delta.z))


@dataclass(frozen=True, eq=True, order=True)
class Delta:
    """A 3D delta, represented as a tuple of (x, y, z).

    For 2D deltas, z should be 0.
    """

    x: int
    y: int
    z: int

    @classmethod
    def zero(cls) -> "Delta":
        return cls(x=0, y=0, z=0)

    @classmethod
    def from_tuple(cls, value: tuple[int, int, int]) -> "Delta":
        (x, y, z) = value
        return cls(x=x, y=y, z=z)

    @classmethod
    def from_coord(cls, coord: Coord) -> "Delta":
        return cls(x=coord.x, y=coord.y, z=coord.z)

    @classmethod
    def from_2d(cls, x: int, y: int) -> "Delta":
        return cls(x=x, y=y, z=0)

    def to_tuple(self) -> tuple[int, int, int]:
        return (self.x, self.y, self.z)

    def to_coord(self) -> Coord:
        return Coord.from_tuple(self.to_tuple())

    def to_2d(self) -> tuple[int, int]:
        assert self.z == 0, "Expected z=0 for 2D delta, got z={}".format(self.z)
        return (self.x, self.y)

    @classmethod
    def parse_from_direction(cls, direction: str) -> "Delta":
        if direction in ["N", "U"]:
            return Deltas2d.NORTH
        elif direction in ["E", "R"]:
            return Deltas2d.EAST
        elif direction in ["S", "D"]:
            return Deltas2d.SOUTH
        elif direction in ["W", "L"]:
            return Deltas2d.WEST
        elif direction in ["NE", "UR"]:
            return Deltas2d.NORTHEAST
        elif direction in ["SE", "DR"]:
            return Deltas2d.SOUTHEAST
        elif direction in ["SW", "DL"]:
            return Deltas2d.SOUTHWEST
        elif direction in ["NW", "UL"]:
            return Deltas2d.NORTHWEST
        else:
            raise ValueError(f"Could not guess delta from direction {direction}")

    def __add__(self, other: "Delta") -> "Delta":
        return Delta(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __mul__(self, scalar: int) -> "Delta":
        return Delta(x=self.x * scalar, y=self.y * scalar, z=self.z * scalar)

    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def chess_distance(self) -> int:
        return max(abs(self.x), abs(self.y), abs(self.z))


class Deltas2d:
    """Constants for common deltas."""

    NORTH = Delta(x=0, y=-1, z=0)
    EAST = Delta(x=1, y=0, z=0)
    SOUTH = Delta(x=0, y=1, z=0)
    WEST = Delta(x=-1, y=0, z=0)

    NORTHEAST = Delta(x=1, y=-1, z=0)
    SOUTHEAST = Delta(x=1, y=1, z=0)
    SOUTHWEST = Delta(x=-1, y=1, z=0)
    NORTHWEST = Delta(x=-1, y=-1, z=0)

    CARDINAL: list[Delta] = [NORTH, EAST, SOUTH, WEST]
    """The four cardinal directions in 2D, represented as a list of deltas.

    The cardinal directions are north/east/south/west.
    """

    ORDINAL: list[Delta] = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
    """The four ordinal directions in 2D, represented as a list of deltas.

    The ordinal directions are north-east/south-east/south-west/north-west.
    """

    ALL: list[Delta] = CARDINAL + ORDINAL
    """All eight directions in 2D, represented as a list of deltas.

    The directions are up/right/down/left/up-right/down-right/down-left/up-left.
    """


@given(st.integers(), st.integers(), st.integers(), st.integers())
def test_delta(x: int, y: int, dx: int, dy: int) -> None:
    coord = Coord.from_2d(x, y)
    delta = Delta.from_2d(dx, dy)
    if delta > Delta.zero():
        assert coord + delta > coord
        assert (coord + delta).manhattan_distance(coord) > 0
        assert (coord + delta).chess_distance(coord) > 0


class DenseGrid(Generic[T]):
    """A 3D grid of values, stored in a list of lists.

    This uses O(n^3) memory, where n is the dimensions of the grid, i.e. it is
    dense.
    """

    def __init__(self, cells: list[list[list[T]]]) -> None:
        self._cells = cells

    @classmethod
    def from_2d(cls, rows: list[list[T]]) -> "DenseGrid[T]":
        """Create a new grid from the given rows.

        The first row is the top row, and the first element of each row is the
        leftmost element. Note that the rows are naturally indexed via (row,
        column), but the grid is indexed via (column, row), i.e. (x, y).
        """
        if not all_same(len(row) for row in rows):
            raise ValueError(
                "All rows must be the same length, but got rows of lengths {}".format(
                    [len(row) for row in rows]
                )
            )
        return cls([rows])

    def __getitem__(self, coord: Coord) -> T:
        """Get the value at the given coordinate."""
        (x, y, z) = coord.to_tuple()
        return self._cells[z][y][x]

    def __setitem__(self, coord: Coord, value: T) -> None:
        """Set the value at the given coordinate."""
        (x, y, z) = coord.to_tuple()
        self._cells[z][y][x] = value

    @property
    def width(self) -> int:
        """The width of the grid, i.e. the number of columns."""
        if len(self._cells) > 0 and len(self._cells[0]) > 0:
            return len(self._cells[0][0])
        else:
            return 0

    @property
    def height(self) -> int:
        """The height of the grid, i.e. the number of rows."""
        if len(self._cells) > 0:
            return len(self._cells[0])
        else:
            return 0

    @property
    def depth(self) -> int:
        """The depth of the grid, i.e. the number of layers."""
        return len(self._cells)

    def is_2d(self) -> bool:
        """Return whether the grid is 2D, i.e. has only one layer."""
        return self.depth == 1

    def iter_left_edge(self) -> Iterable[tuple[Coord, T]]:
        """Iterate over the left edge of the grid, from top to bottom."""
        assert self.is_2d()
        for y in range(self.height):
            coord = Coord(0, y, 0)
            yield (coord, self[coord])

    def iter_right_edge(self) -> Iterable[tuple[Coord, T]]:
        """Iterate over the right edge of the grid, from top to bottom."""
        assert self.is_2d()
        for y in range(self.height):
            coord = Coord(self.width - 1, y, 0)
            yield (coord, self[coord])

    def iter_vertical_edges(self) -> Iterable[tuple[Coord, T]]:
        """Iterate over the left and right edges of the grid, from top to
        bottom.

        Note that duplicate coordinates are not yielded (in the situation where
        the grid is only one column wide).
        """
        return unique_ordered(
            itertools.chain(self.iter_left_edge(), self.iter_right_edge())
        )

    def iter_top_edge(self) -> Iterable[tuple[Coord, T]]:
        """Iterate over the top edge of the grid, from left to right."""
        assert self.is_2d()
        for x in range(self.width):
            coord = Coord(x, 0, 0)
            yield (coord, self[coord])

    def iter_bottom_edge(self) -> Iterable[tuple[Coord, T]]:
        """Iterate over the bottom edge of the grid, from left to right."""
        assert self.is_2d()
        for x in range(self.width):
            coord = Coord(x, self.height - 1, 0)
            yield (coord, self[coord])

    def iter_horizontal_edges(self) -> Iterable[tuple[Coord, T]]:
        """Iterate over the top and bottom edges of the grid, from left to
        right.

        Note that duplicate coordinates are not yielded (in the situation where
        the grid is only one row tall).
        """
        return unique_ordered(
            itertools.chain(self.iter_top_edge(), self.iter_bottom_edge())
        )

    def iter_edges(self) -> Iterable[tuple[Coord, T]]:
        """Iterate over all edges of the grid, from left to right, then top to
        bottom.

        Note that duplicate coordinates are not yielded.
        """
        return unique_ordered(
            itertools.chain(self.iter_horizontal_edges(), self.iter_vertical_edges())
        )

    def iter_coords(self) -> Iterable[Coord]:
        """Iterate over all coordinates in the grid, in some order."""
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    yield Coord(x, y, z)

    def iter_cells(self) -> Iterable[tuple[Coord, T]]:
        """Iterate over all coordinates and values in the grid, in some
        order.
        """
        for coord in self.iter_coords():
            yield (coord, self[coord])

    def iter_delta(
        self,
        start: Coord,
        delta: Delta,
        *,
        include_start: bool = True,
    ) -> Iterable[tuple[Coord, T]]:
        """Iterate over all coordinates and values in the grid, starting at
        the given coordinate and moving in the given direction.

        If include_start is False, the start coordinate is not yielded.
        """
        (x, y, z) = start.to_tuple()
        (dx, dy, dz) = delta.to_tuple()
        while 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            coord = Coord(x, y, z)
            if coord == start and not include_start:
                pass
            else:
                yield (coord, self[coord])
            x += dx
            y += dy
            z += dz

    def iter_deltas(
        self,
        start: Coord,
        deltas: Iterable[Delta],
        *,
        include_start: bool = True,
    ) -> Iterable[tuple[Coord, T, Delta]]:
        """Iterate over all coordinates and values in the grid, starting at
        the given coordinate and moving in the given directions.

        If include_start is False, the start coordinate is not yielded.
        """
        for delta in deltas:
            for (coord, value) in self.iter_delta(
                start=start, delta=delta, include_start=include_start
            ):
                yield (coord, value, delta)


def test_grid() -> None:
    C = Coord.from_2d
    D = Delta.from_2d

    with pytest.raises(ValueError, match="All rows must be the same length"):
        DenseGrid.from_2d([["a", "b"], ["c"]])

    grid = DenseGrid.from_2d([["a", "b"], ["c", "d"]])
    assert grid[C(0, 0)] == "a"
    assert grid[C(1, 0)] == "b"
    assert grid[C(0, 1)] == "c"
    assert grid[C(1, 1)] == "d"
    assert grid.width == 2
    assert grid.height == 2

    assert list(grid.iter_left_edge()) == [(C(0, 0), "a"), (C(0, 1), "c")]
    assert list(grid.iter_right_edge()) == [(C(1, 0), "b"), (C(1, 1), "d")]
    assert list(grid.iter_vertical_edges()) == [
        (C(0, 0), "a"),
        (C(0, 1), "c"),
        (C(1, 0), "b"),
        (C(1, 1), "d"),
    ]
    assert list(grid.iter_top_edge()) == [(C(0, 0), "a"), (C(1, 0), "b")]
    assert list(grid.iter_bottom_edge()) == [(C(0, 1), "c"), (C(1, 1), "d")]
    assert list(grid.iter_horizontal_edges()) == [
        (C(0, 0), "a"),
        (C(1, 0), "b"),
        (C(0, 1), "c"),
        (C(1, 1), "d"),
    ]
    assert list(grid.iter_edges()) == [
        (C(0, 0), "a"),
        (C(1, 0), "b"),
        (C(0, 1), "c"),
        (C(1, 1), "d"),
    ]

    assert list(grid.iter_coords()) == [C(0, 0), C(1, 0), C(0, 1), C(1, 1)]
    assert list(grid.iter_cells()) == [
        (C(0, 0), "a"),
        (C(1, 0), "b"),
        (C(0, 1), "c"),
        (C(1, 1), "d"),
    ]
    assert list(grid.iter_delta(C(0, 0), D(1, 0))) == [
        (C(0, 0), "a"),
        (C(1, 0), "b"),
    ]
    assert list(grid.iter_delta(C(0, 0), D(1, 0), include_start=False)) == [
        (C(1, 0), "b"),
    ]
    assert list(grid.iter_delta(C(0, 0), D(1, 1))) == [
        (C(0, 0), "a"),
        (C(1, 1), "d"),
    ]
    assert list(grid.iter_delta(C(0, 0), D(1, 1), include_start=False)) == [
        (C(1, 1), "d"),
    ]
    assert list(grid.iter_deltas(C(0, 0), [D(1, 0), D(1, 1)])) == [
        (C(0, 0), "a", D(1, 0)),
        (C(1, 0), "b", D(1, 0)),
        (C(0, 0), "a", D(1, 1)),
        (C(1, 1), "d", D(1, 1)),
    ]
    assert list(grid.iter_deltas(C(0, 0), [D(1, 0), D(1, 1)], include_start=False)) == [
        (C(1, 0), "b", D(1, 0)),
        (C(1, 1), "d", D(1, 1)),
    ]


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
