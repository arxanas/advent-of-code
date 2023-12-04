import collections
import itertools
from dataclasses import dataclass
from typing import Generic, Iterable, Optional, TypeVar, overload

import pytest
from hypothesis import given
from hypothesis import strategies as st

from . import all_same, minmax, unique_ordered

T = TypeVar("T")
U = TypeVar("U")


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

    def north(self) -> "Coord":
        return self + Deltas2d.NORTH

    def east(self) -> "Coord":
        return self + Deltas2d.EAST

    def south(self) -> "Coord":
        return self + Deltas2d.SOUTH

    def west(self) -> "Coord":
        return self + Deltas2d.WEST

    def between(self, other: "Coord") -> Iterable["Coord"]:
        (min_x, max_x) = sorted((self.x, other.x))
        (min_y, max_y) = sorted((self.y, other.y))
        (min_z, max_z) = sorted((self.z, other.z))
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    yield Coord(x=x, y=y, z=z)


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


class Deltas3d:
    CARDINAL = Deltas2d.CARDINAL + [Delta(x=0, y=0, z=1), Delta(x=0, y=0, z=-1)]
    """The six cardinal directions in 3D, represented as a list of deltas.

    The cardinal directions are north/east/south/west/in/out.
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

    def __contains__(self, coord: Coord) -> bool:
        """Return whether the given coordinate is in the grid."""
        (x, y, z) = coord.to_tuple()
        return 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth

    @overload
    def get(self, coord: Coord, default: U) -> T | U:
        ...

    @overload
    def get(self, coord: Coord) -> T | None:
        ...

    def get(self, coord: Coord, default: object = None) -> object:
        """Get the value at the given coordinate, or `None` if the coordinate is
        not in the grid.
        """
        if coord in self:
            return self[coord]
        else:
            return default

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
        max_steps: Optional[int] = None,
    ) -> Iterable[tuple[Coord, T]]:
        """Iterate over all coordinates and values in the grid, starting at
        the given coordinate and moving in the given direction.

        If `include_start` is False, the start coordinate is not yielded.
        If `max_steps` is not None, at most `max_steps` coordinates are yielded.
        (Note that this interacts with `include_start` to include or exclude the
        start coordinate.)
        """
        (x, y, z) = start.to_tuple()
        (dx, dy, dz) = delta.to_tuple()
        i = 0
        while 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            coord = Coord(x, y, z)
            if coord == start and not include_start:
                pass
            else:
                i += 1
                if max_steps is not None and i > max_steps:
                    return
                yield (coord, self[coord])
            x += dx
            y += dy
            z += dz

    def iter_deltas(
        self,
        start: Coord,
        deltas: Iterable[Delta],
        *,
        max_steps: Optional[int] = None,
    ) -> Iterable[tuple[Coord, T, Delta]]:
        """Iterate over all coordinates and values in the grid, starting at
        the given coordinate and moving in the given directions.

        See `iter_delta` for the meanings of the keyword parameters. The value
        of `include_start` is always set to `False`, since it would otherwise be
        included in multiple results.
        """
        for delta in deltas:
            for coord, value in self.iter_delta(
                start=start,
                delta=delta,
                include_start=False,
                max_steps=max_steps,
            ):
                yield (coord, value, delta)


def test_dense_grid() -> None:
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
        (C(1, 0), "b", D(1, 0)),
        (C(1, 1), "d", D(1, 1)),
    ]


def test_dense_grid_iter_deltas_max_steps() -> None:
    C = Coord.from_2d
    D = Delta.from_2d

    grid = DenseGrid.from_2d(
        [["a", "b", "c", "d"], ["e", "f", "g", "h"], ["i", "j", "k", "l"]]
    )
    assert list(grid.iter_deltas(C(0, 0), [D(1, 0), D(0, 1)], max_steps=1)) == [
        (C(1, 0), "b", D(1, 0)),
        (C(0, 1), "e", D(0, 1)),
    ]
    assert list(grid.iter_deltas(C(0, 0), [D(1, 0), D(0, 1)], max_steps=2)) == [
        (C(1, 0), "b", D(1, 0)),
        (C(2, 0), "c", D(1, 0)),
        (C(0, 1), "e", D(0, 1)),
        (C(0, 2), "i", D(0, 1)),
    ]


class SparseGrid(Generic[T]):
    def __init__(self, cells: dict[Coord, T]) -> None:
        self._cells = cells

    def __repr__(self) -> str:
        return "SparseGrid({!r})".format(self._cells)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SparseGrid) and self._cells == other._cells

    def __getitem__(self, coord: Coord) -> T:
        """Get the value at the given coordinate."""
        return self._cells[coord]

    def __setitem__(self, coord: Coord, value: T) -> None:
        """Set the value at the given coordinate."""
        self._cells[coord] = value

    def __delitem__(self, coord: Coord) -> None:
        """Delete the value at the given coordinate."""
        del self._cells[coord]

    def __contains__(self, coord: Coord) -> bool:
        """Return whether the given coordinate has been assigned in the grid."""
        return coord in self._cells

    def __len__(self) -> int:
        """Return the number of coordinates that have been assigned in the
        grid.
        """
        return len(self._cells)

    def width(self) -> int:
        """Return the implied width of the grid, starting from the coordinate with the
        least x-coordinate and ending at the coordinate with the greatest x-coordinate.
        """
        (min_x, max_x) = minmax(c.x for c in self._cells.keys())
        return max_x - min_x + 1

    def height(self) -> int:
        """Return the implied height of the grid, starting from the coordinate with the
        least y-coordinate and ending at the coordinate with the greatest y-coordinate.
        """
        (min_y, max_y) = minmax(c.y for c in self._cells.keys())
        return max_y - min_y + 1

    def dump(self) -> str:
        """Dump the grid to a string, with the top row first."""
        if len(self._cells) == 0:
            return ""
        (min_x, max_x) = minmax(c.x for c in self._cells.keys())
        (min_y, max_y) = minmax(c.y for c in self._cells.keys())
        lines = []
        for y in range(min_y, max_y + 1):
            line = []
            for x in range(min_x, max_x + 1):
                line.append(str(self._cells.get(Coord(x, y, 0), ".")))
            lines.append("".join(line))
        return "\n".join(lines)

    def copy(self) -> "SparseGrid[T]":
        """Return a copy of the grid."""
        return SparseGrid(cells=self._cells.copy())

    @overload
    def get(self, coord: Coord, default: U) -> T | U:
        ...

    @overload
    def get(self, coord: Coord) -> T | None:
        ...

    def get(self, coord: Coord, default: object = None) -> object:
        """Get the value at the given coordinate, or `None` if the coordinate is
        not in the grid.
        """
        return self._cells.get(coord, default)

    def iter_cells(self) -> Iterable[tuple[Coord, T]]:
        """Iterate over all coordinates and values in the grid, in some
        order.
        """
        for coord, value in self._cells.items():
            yield (coord, value)


class ShortestPath(Generic[T]):
    """Generic shortest path algorithm.

    You should subclass this class and override the `get_neighbors` method.

    Only integral distances are supported. The graph must be finite, or at
    least, the `get_neighbors` method should produce a finite subgraph of the
    original graph when queried.
    """

    def __init__(self) -> None:
        self._best_lengths: dict[T, tuple[int, list[T]]] = {}

    def get_neighbors(self, node: T) -> list[tuple[T, int]]:
        """Returns a list of (neighbor, distance) pairs for the given node.

        Should be overridden by the implementor.
        """
        raise NotImplementedError

    def run(
        self, start_nodes: list[T], end_nodes: list[T]
    ) -> dict[T, tuple[int, list[T]]]:
        """Find the shortest paths from any of the start nodes to any of the end
        nodes.

        Returns a dictionary mapping each end node to a tuple of the length of
        the shortest path and the path itself. If no path exists for a given end
        node, there will be no entry in the dictionary for that node. If
        multiple shortest paths exist, it is not specified which one will be
        returned.
        """
        self._best_lengths = {node: (0, [node]) for node in start_nodes}
        end_nodes2 = set(end_nodes)
        queue = collections.deque[T](start_nodes)
        while queue:
            current_node = queue.popleft()
            if current_node in end_nodes2:
                continue
            (current_length, current_path) = self._best_lengths[current_node]
            for neighbor, distance in self.get_neighbors(current_node):
                new_length = current_length + distance
                should_enqueue = False
                neighbor_info = self._best_lengths.get(neighbor)
                if neighbor_info is None:
                    should_enqueue = True
                else:
                    (neighbor_length, _neighbor_path) = neighbor_info
                    if new_length < neighbor_length:
                        should_enqueue = True
                if should_enqueue:
                    self._best_lengths[neighbor] = (
                        new_length,
                        current_path + [neighbor],
                    )
                    queue.append(neighbor)

        return {k: v for (k, v) in self._best_lengths.items() if k in end_nodes2}


def test_shortest_path() -> None:
    class MyShortestPath(ShortestPath[int]):
        def get_neighbors(self, node: int) -> list[tuple[int, int]]:
            if node >= 20:
                return []
            else:
                return [(node + 2, 2), (node + 3, 3)]

    shortest_path = MyShortestPath()
    assert shortest_path.run([1], [9]) == {9: (8, [1, 3, 6, 9])}
