from dataclasses import dataclass, replace
from functools import *
from itertools import *

from .. import utils as u

Input = u.DenseGrid[int]

TEST_INPUT1 = r"""
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

TEST_INPUT2 = TEST_INPUT1

PART_1_ANSWER = 102
PART_2_ANSWER = 94


def test_part1() -> None:
    assert Solution().part1(Solution().parse_input(TEST_INPUT1)) == PART_1_ANSWER


def test_part2() -> None:
    assert Solution().part2(Solution().parse_input(TEST_INPUT2)) == PART_2_ANSWER
    assert (
        Solution().part2(
            Solution().parse_input(
                r"""

111111111111
999999999991
999999999991
999999999991
999999999991
"""
            )
        )
        == 71
    )


@dataclass(frozen=True)
class Node:
    coord: u.Coord
    delta: u.Delta
    num_moves_in_this_direction: int


class Solution(u.Solution[Input]):
    def parse_input(self, input: str) -> Input:
        return u.DenseGrid.from_str_mapped(input, int)

    def part1(self, input: Input) -> int:
        top_left = u.Coord.from_2d(0, 0)
        bottom_right = u.Coord.from_2d(input.width - 1, input.height - 1)

        class ShortestPath(u.ShortestPath[Node]):
            def is_end_node(self, node: Node) -> bool:
                return node.coord == bottom_right

            def get_neighbors(self, node: Node) -> list[tuple[Node, int]]:
                next_nodes = [
                    Node(
                        coord=node.coord + node.delta.rotate_left(),
                        delta=node.delta.rotate_left(),
                        num_moves_in_this_direction=1,
                    ),
                    Node(
                        coord=node.coord + node.delta.rotate_right(),
                        delta=node.delta.rotate_right(),
                        num_moves_in_this_direction=1,
                    ),
                ]
                if node.num_moves_in_this_direction < 3:
                    next_nodes.append(
                        replace(
                            node,
                            coord=node.coord + node.delta,
                            num_moves_in_this_direction=node.num_moves_in_this_direction
                            + 1,
                        )
                    )

                return [
                    (next_node, weight)
                    for next_node in next_nodes
                    if (weight := input.get(next_node.coord)) is not None
                ]

        shortest_path = ShortestPath()
        result = shortest_path.run(
            start_nodes=[
                Node(
                    coord=top_left, delta=u.Deltas2d.EAST, num_moves_in_this_direction=1
                ),
                Node(
                    coord=top_left,
                    delta=u.Deltas2d.SOUTH,
                    num_moves_in_this_direction=1,
                ),
            ],
        )
        return next(weight for (weight, _path) in result.values())

    def part2(self, input: Input) -> int:
        top_left = u.Coord.from_2d(0, 0)
        bottom_right = u.Coord.from_2d(input.width - 1, input.height - 1)

        class ShortestPath(u.ShortestPath[Node]):
            def _can_turn_or_stop(self, node: Node) -> bool:
                return node.num_moves_in_this_direction >= 4

            def is_end_node(self, node: Node) -> bool:
                return node.coord == bottom_right and self._can_turn_or_stop(node)

            def get_neighbors(self, node: Node) -> list[tuple[Node, int]]:
                next_nodes = []
                if self._can_turn_or_stop(node):
                    next_nodes.extend(
                        [
                            Node(
                                coord=node.coord + node.delta.rotate_left(),
                                delta=node.delta.rotate_left(),
                                num_moves_in_this_direction=1,
                            ),
                            Node(
                                coord=node.coord + node.delta.rotate_right(),
                                delta=node.delta.rotate_right(),
                                num_moves_in_this_direction=1,
                            ),
                        ]
                    )
                if node.num_moves_in_this_direction < 10:
                    next_nodes.append(
                        Node(
                            coord=node.coord + node.delta,
                            delta=node.delta,
                            num_moves_in_this_direction=node.num_moves_in_this_direction
                            + 1,
                        )
                    )

                return [
                    (next_node, weight)
                    for next_node in next_nodes
                    if (weight := input.get(next_node.coord)) is not None
                ]

        shortest_path = ShortestPath()
        result = shortest_path.run(
            start_nodes=[
                Node(
                    coord=top_left, delta=u.Deltas2d.EAST, num_moves_in_this_direction=1
                ),
                Node(
                    coord=top_left,
                    delta=u.Deltas2d.SOUTH,
                    num_moves_in_this_direction=1,
                ),
            ],
        )
        return next(weight for (weight, _path) in result.values())
