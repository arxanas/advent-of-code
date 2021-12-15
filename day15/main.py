import sys
from collections import *
from functools import *
from typing import *
from dataclasses import dataclass
import heapq

TEST_INPUT = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

Input = Dict[Tuple[int, int], int]


def neighbors(grid: Input, row: int, col: int) -> Iterable[Tuple[int, int]]:
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if (dr == 0 and dc != 0) or (dc == 0 and dr != 0):
                r2 = row + dr
                c2 = col + dc
                if (r2, c2) in grid:
                    yield (r2, c2)


Point = Tuple[int, int]


@dataclass(order=True)
class Node:
    distance: int
    is_dummy: bool
    index: Point


def shortest_path(grid: Input, dim: int) -> int:
    unvisited = set(grid.keys())
    first_node = Node(index=(0, 0), is_dummy=False, distance=0)
    nearest_neighbors: List[Node] = []
    best_distances = {(0, 0): first_node}
    row = 0
    col = 0
    while (row, col) != (dim - 1, dim - 1):
        unvisited.remove((row, col))

        for neighbor in neighbors(grid=grid, row=row, col=col):
            if neighbor in unvisited:
                tentative_distance = best_distances[row, col].distance + grid[neighbor]

                if neighbor not in best_distances:
                    node = Node(
                        index=neighbor, is_dummy=False, distance=tentative_distance
                    )
                    best_distances[neighbor] = node
                    heapq.heappush(nearest_neighbors, node)

                elif (
                    neighbor in best_distances
                    and tentative_distance < best_distances[neighbor].distance
                ):
                    best_distances[neighbor].is_dummy = True
                    node = Node(
                        distance=tentative_distance, is_dummy=False, index=neighbor
                    )
                    best_distances[neighbor] = node
                    heapq.heappush(nearest_neighbors, node)

        while (x := heapq.heappop(nearest_neighbors)).is_dummy:
            pass
        (row, col) = x.index
    return best_distances[dim - 1, dim - 1].distance


def part1(input: Input) -> str:
    dim = int(len(input) ** 0.5)
    return str(shortest_path(input, dim))


def part2(small_input: Input) -> str:
    small_dim = int(len(small_input) ** 0.5)
    input = {}
    for dr in range(5):
        for dc in range(5):
            for ((r, c), cost) in small_input.items():
                c2 = cost + dr + dc
                while c2 > 9:
                    c2 -= 9
                input[r + (small_dim * dr), c + (small_dim * dc)] = c2
    return part1(input)


def parse_input(input: str) -> Input:
    grid = {}
    for (row, line) in enumerate(input.strip().splitlines()):
        for (col, c) in enumerate(line):
            grid[row, col] = int(c)
    return grid


def main() -> None:
    input = parse_input(sys.stdin.read())
    test_input = parse_input(TEST_INPUT)

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
