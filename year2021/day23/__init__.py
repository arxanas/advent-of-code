from __future__ import annotations

import sys
from collections import Counter
from dataclasses import dataclass, replace
from typing import Dict, Iterable, List, Optional, cast

# DEBUG = True
DEBUG = False

TEST_INPUT = [["A", "B"], ["D", "C"], ["C", "B"], ["A", "D"]]
TEST_INPUT2 = [
    ["A", "D", "D", "B"],
    ["D", "B", "C", "C"],
    ["C", "A", "B", "B"],
    ["A", "C", "A", "D"],
]
INPUT = [["C", "B"], ["A", "B"], ["D", "D"], ["C", "A"]]
INPUT2 = [
    ["C", "D", "D", "B"],
    ["A", "B", "C", "B"],
    ["D", "A", "B", "D"],
    ["C", "C", "A", "A"],
]
COSTS = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}
BANKS = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
}
HALLWAY_LENGTH = 11
VALID_HALLWAY_INDEXES = [0, 1, 3, 5, 7, 9, 10]
BANK_INDEXES = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}


@dataclass(frozen=True, eq=True)
class State:
    prev_state: Optional["State"]
    used_energy: int
    hallway: List[Optional[str]]
    banks: Dict[str, List[str]]


def get_moves_to_bank(state: State, bank_size: int) -> Iterable[State]:
    for hallway_index, amph in enumerate(state.hallway):
        if amph is None:
            continue
        target_bank = BANK_INDEXES[amph]
        if hallway_index <= target_bank:
            is_path_clear = all(
                cell is None
                for cell in state.hallway[hallway_index + 1 : target_bank + 1]
            )
        else:
            is_path_clear = all(
                cell is None for cell in state.hallway[target_bank:hallway_index]
            )
        if is_path_clear and all(
            other_amph == amph for other_amph in state.banks[amph]
        ):
            distance = int(abs(target_bank - hallway_index)) + (
                bank_size - len(state.banks[amph])
            )
            used_energy = state.used_energy + (distance * COSTS[amph])
            hallway = list(state.hallway)
            hallway[hallway_index] = None
            banks = dict(state.banks)
            banks[amph] = list(banks[amph])
            banks[amph].append(amph)
            yield replace(state, used_energy=used_energy, hallway=hallway, banks=banks)


def get_moves_to_hallway(state: State, bank_size: int) -> Iterable[State]:
    for bank_index, amphs in state.banks.items():
        if not amphs:
            continue
        if all(bank_amph == bank_index for bank_amph in amphs):
            continue
        amph = amphs[-1]
        starting_index = BANK_INDEXES[bank_index]
        for hallway_index in VALID_HALLWAY_INDEXES:
            if starting_index <= hallway_index:
                is_path_clear = all(
                    cell is None
                    for cell in state.hallway[starting_index : hallway_index + 1]
                )
            else:
                is_path_clear = all(
                    cell is None
                    for cell in state.hallway[hallway_index : starting_index + 1]
                )
            if is_path_clear:
                distance = (
                    int(abs(hallway_index - starting_index))
                    + 1
                    + (bank_size - len(amphs))
                )
                used_energy = state.used_energy + (distance * COSTS[amph])
                hallway = list(state.hallway)
                hallway[hallway_index] = amph
                banks = dict(state.banks)
                banks[bank_index] = list(banks[bank_index])
                popped_amph = banks[bank_index].pop()
                assert popped_amph == amph
                yield replace(
                    state, used_energy=used_energy, hallway=hallway, banks=banks
                )

                if (
                    starting_index <= hallway_index
                    and hallway_index == BANK_INDEXES[amph] + 1
                ) or (
                    starting_index >= hallway_index
                    and hallway_index == BANK_INDEXES[amph] - 1
                ):
                    if all(other_amph == amph for other_amph in state.banks[amph]):
                        distance += bank_size - 1 - len(state.banks[amph])
                        used_energy = state.used_energy + (distance * COSTS[amph])

                        banks = dict(state.banks)
                        banks[bank_index] = list(banks[bank_index])
                        popped_amph = banks[bank_index].pop()
                        banks[amph] = list(banks[amph])
                        banks[amph].append(amph)

                        yield replace(
                            state,
                            used_energy=used_energy,
                            hallway=state.hallway,
                            banks=banks,
                        )


def get_next_states(state: State, bank_size: int) -> Iterable[State]:
    yield from get_moves_to_bank(state, bank_size=bank_size)
    yield from get_moves_to_hallway(state, bank_size=bank_size)


def test_get_next_states() -> None:
    hallway: List[Optional[str]] = [None] * HALLWAY_LENGTH
    s1 = State(
        prev_state=None,
        used_energy=0,
        hallway=hallway,
        banks={
            "A": ["A", "B"],
            "B": ["D", "C"],
            "C": ["C", "B"],
            "D": ["A", "D"],
        },
    )
    hallway = list(hallway)
    hallway[3] = "B"
    s2 = State(
        prev_state=None,
        used_energy=40,
        hallway=hallway,
        banks={
            "A": ["A", "B"],
            "B": ["D", "C"],
            "C": ["C"],
            "D": ["A", "D"],
        },
    )
    assert s2 in list(get_next_states(s1, bank_size=2))

    s3 = State(
        prev_state=None,
        used_energy=440,
        hallway=hallway,
        banks={
            "A": ["A", "B"],
            "B": ["D"],
            "C": ["C", "C"],
            "D": ["A", "D"],
        },
    )
    assert s3 in list(get_next_states(s2, bank_size=2))

    hallway = list(hallway)
    hallway[5] = "D"
    s4 = State(
        prev_state=None,
        used_energy=3440,
        hallway=hallway,
        banks={
            "A": ["A", "B"],
            "B": [],
            "C": ["C", "C"],
            "D": ["A", "D"],
        },
    )
    assert s4 in list(get_next_states(s3, bank_size=2))

    hallway = list(hallway)
    hallway[3] = None
    s5 = State(
        prev_state=None,
        used_energy=3470,
        hallway=hallway,
        banks={
            "A": ["A", "B"],
            "B": ["B"],
            "C": ["C", "C"],
            "D": ["A", "D"],
        },
    )
    assert s5 in list(get_next_states(s4, bank_size=2))


def is_solved(state: State, bank_size: int) -> bool:
    return all(v == [k] * bank_size for (k, v) in state.banks.items())


def get_state_key(state: State) -> object:
    return (
        state.used_energy,
        tuple(state.hallway),
        tuple((k, tuple(v)) for (k, v) in state.banks.items()),
    )


def search(input: List[List[str]], bank_size: int) -> int:
    initial_state = State(
        prev_state=None,
        used_energy=0,
        hallway=[None] * HALLWAY_LENGTH,
        banks={
            "A": input[0],
            "B": input[1],
            "C": input[2],
            "D": input[3],
        },
    )

    seen_states = set()
    q = [initial_state]
    best_solution = None
    while q:
        state = q.pop()
        state_key = get_state_key(state)
        if state_key in seen_states:
            continue
        seen_states.add(state_key)

        if is_solved(state, bank_size=bank_size):
            if best_solution is None:
                best_solution = state
            else:
                best_solution = min(
                    state, best_solution, key=lambda x: cast(State, x).used_energy
                )
        elif (
            best_solution is not None and state.used_energy >= best_solution.used_energy
        ):
            continue

        for next_state in get_next_states(state, bank_size=bank_size):
            if DEBUG:
                counts: Dict[str, int] = Counter()
                for amph in next_state.hallway:
                    if amph is not None:
                        counts[amph] += 1
                for bank in next_state.banks.values():
                    for amph in bank:
                        counts[amph] += 1
                if counts != {
                    "A": bank_size,
                    "B": bank_size,
                    "C": bank_size,
                    "D": bank_size,
                }:
                    print("Bad state transition")
                    print("Counts:", counts)
                    print("Old state:", state)
                    print("New state:", next_state)
                    sys.exit(1)
            next_state = replace(next_state, prev_state=state)
            q.append(next_state)

    assert best_solution is not None
    prev_states = []
    prev_state: Optional[State] = best_solution
    while prev_state is not None:
        prev_states.append(replace(prev_state, prev_state=None))
        prev_state = prev_state.prev_state
    prev_states.reverse()
    return best_solution.used_energy


def part1(input: List[List[str]]) -> int:
    return search(input, bank_size=2)


def part2(input: List[List[str]]) -> int:
    return search(input, bank_size=4)


def main() -> None:
    print(part1(TEST_INPUT))
    print(part1(INPUT))
    print(part2(TEST_INPUT2))
    print(part2(INPUT2))


if __name__ == "__main__":
    main()
