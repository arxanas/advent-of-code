import sys
from collections import *
from functools import *
from typing import *
from dataclasses import dataclass
import math

TEST_INPUT = {1: 4, 2: 8}


Input = Dict[int, int]


def dice_rolls():
    while True:
        for i in range(100):
            yield i + 1


def part1(input: Input) -> object:
    rolls = dice_rolls()
    players = dict(input)
    scores = {
        1: 0,
        2: 0,
    }
    num_die_rolls = 0
    should_continue = True
    while should_continue:
        for player in players:
            roll = sum([next(rolls), next(rolls), next(rolls)])
            num_die_rolls += 3
            players[player] += roll
            while players[player] > 10:
                players[player] -= 10
            scores[player] += players[player]
            if scores[player] >= 1000:
                should_continue = False
                break
    losing_score = min(scores.values())
    return num_die_rolls * losing_score


@cache
def quantum_play(
    turn: int,
    player1_pos: int,
    player2_pos: int,
    player1_score: int,
    player2_score: int,
) -> Dict[int, int]:
    if player1_score >= 21:
        return {1: 1, 2: 0}
    elif player2_score >= 21:
        return {1: 0, 2: 1}

    players = {
        1: player1_pos,
        2: player2_pos,
    }
    scores = {
        1: player1_score,
        2: player2_score,
    }
    num_universes = Counter(
        {
            1: 0,
            2: 0,
        }
    )

    for die1 in [1, 2, 3]:
        for die2 in [1, 2, 3]:
            for die3 in [1, 2, 3]:
                roll = die1 + die2 + die3
                old_player = players[turn]
                players[turn] += roll
                while players[turn] > 10:
                    players[turn] -= 10
                old_score = scores[turn]
                scores[turn] += players[turn]
                num_universes.update(
                    quantum_play(
                        turn=3 - turn,
                        player1_pos=players[1],
                        player2_pos=players[2],
                        player1_score=scores[1],
                        player2_score=scores[2],
                    )
                )
                scores[turn] = old_score
                players[turn] = old_player

    return num_universes


def part2(input: Input) -> object:
    result = quantum_play(
        turn=1,
        player1_pos=input[1],
        player2_pos=input[2],
        player1_score=0,
        player2_score=0,
    )
    return max(result.values())


def main() -> None:
    input = {
        1: 7,
        2: 4,
    }
    test_input = TEST_INPUT

    print("test 1:", part1(test_input))
    print("part 1:", part1(input))
    print("test 2:", part2(test_input))
    print("part 2:", part2(input))


if __name__ == "__main__":
    main()
